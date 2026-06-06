"""
Retrieval module for RAG-based Teaching Assistant.
Handles embedding generation, similarity search, and result ranking.
"""

import requests
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict


class EmbeddingEngine:
    """Creates embeddings using Ollama's BGE-M3 model."""
    
    def __init__(self, model: str = "bge-m3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/embed"
    
    def create_embeddings(self, text_list: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts using Ollama.
        
        Args:
            text_list: List of text strings to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            ConnectionError: If Ollama service is not available
            ValueError: If embedding creation fails
        """
        try:
            response = requests.post(self.api_endpoint, json={
                "model": self.model,
                "input": text_list
            }, timeout=30)
            
            if response.status_code != 200:
                raise ValueError(f"Ollama API error: {response.text}")
            
            embeddings = response.json()["embeddings"]
            return embeddings
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running: ollama serve"
            )


class RAGRetriever:
    """Retrieval system for RAG-based answers."""
    
    def __init__(self, embeddings_path: str = "embeddings.joblib"):
        """
        Initialize retriever with pre-computed embeddings.
        
        Args:
            embeddings_path: Path to the joblib file with embeddings
            
        Raises:
            FileNotFoundError: If embeddings file not found
        """
        try:
            self.df = joblib.load(embeddings_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Embeddings file not found: {embeddings_path}. "
                "Run preprocess_json.py first to generate embeddings."
            )
        
        self.embedding_engine = EmbeddingEngine()
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve top-K most relevant chunks for a query.
        
        Args:
            query: User query string
            top_k: Number of results to return
            
        Returns:
            List of dictionaries with chunk data and similarity scores
        """
        # Create embedding for query
        query_embedding = self.embedding_engine.create_embeddings([query])[0]
        
        # Compute similarities
        chunk_embeddings = np.vstack(self.df['embedding'].values)
        similarities = cosine_similarity(
            chunk_embeddings, 
            [query_embedding]
        ).flatten()
        
        # Get top-k indices
        top_indices = similarities.argsort()[::-1][:top_k]
        
        # Prepare results with metadata
        results = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            results.append({
                'chunk_id': row.get('chunk_id', idx),
                'title': row.get('title', 'Unknown'),
                'number': row.get('number', 'N/A'),
                'text': row.get('text', ''),
                'start': row.get('start', 0),
                'end': row.get('end', 0),
                'similarity_score': float(similarities[idx])
            })
        
        return results
    
    def format_context(self, results: List[Dict]) -> str:
        """
        Format retrieved results into a context string for the LLM.
        
        Args:
            results: List of retrieved chunks
            
        Returns:
            Formatted context string
        """
        context = "Video chunks containing relevant information:\n\n"
        for i, result in enumerate(results, 1):
            timestamp = self._format_timestamp(result['start'], result['end'])
            context += f"{i}. [{result['title']} - Video {result['number']}] ({timestamp})\n"
            context += f"   Relevance: {result['similarity_score']:.2%}\n"
            context += f"   Text: {result['text'][:200]}...\n\n"
        return context
    
    @staticmethod
    def _format_timestamp(start: float, end: float) -> str:
        """Convert seconds to MM:SS format."""
        def seconds_to_mmss(sec):
            minutes = int(sec // 60)
            seconds = int(sec % 60)
            return f"{minutes}:{seconds:02d}"
        
        return f"{seconds_to_mmss(start)} - {seconds_to_mmss(end)}"
    
    def get_source_links(self, results: List[Dict]) -> str:
        """
        Generate source attribution with timestamps.
        
        Args:
            results: List of retrieved chunks
            
        Returns:
            Formatted source attribution string
        """
        sources = "📚 Source References:\n"
        for result in results:
            timestamp = self._format_timestamp(result['start'], result['end'])
            sources += f"- {result['title']} (Video {result['number']}) @ {timestamp}\n"
        return sources
