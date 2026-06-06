"""
LLM Inference module for RAG-based Teaching Assistant.
Uses Ollama's local models (deepseek-r1) for response generation.
"""

import requests
from typing import Optional


class OllamaLLM:
    """Local LLM inference using Ollama."""
    
    def __init__(self, 
                 model: str = "deepseek-r1:1.5b",
                 base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama LLM.
        
        Args:
            model: Model name in Ollama
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: Input prompt for the model
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Generated response text
            
        Raises:
            ConnectionError: If Ollama is not available
            ValueError: If generation fails
        """
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature
                },
                timeout=120
            )
            
            if response.status_code != 200:
                raise ValueError(f"Ollama error: {response.text}")
            
            result = response.json()
            return result.get("response", "").strip()
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running: ollama serve"
            )


def build_rag_prompt(query: str, context: str, course_name: str = "Web Development") -> str:
    """
    Build a RAG prompt for the LLM.
    
    Args:
        query: User's question
        context: Retrieved context from the knowledge base
        course_name: Name of the course
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a helpful teaching assistant for the {course_name} course.
    
A student asked: "{query}"

Here is relevant information from the course lectures:
{context}

Instructions:
1. Answer the question in a clear, helpful way
2. Reference the specific video(s) and timestamps where the content is taught
3. If the question is not related to {course_name}, politely explain that you can only answer course-related questions
4. Keep your answer concise and focused

Answer:"""
    
    return prompt
