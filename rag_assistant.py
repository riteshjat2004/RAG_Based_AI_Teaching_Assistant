"""
CLI Interface for RAG-based Teaching Assistant.
Simple command-line interface for querying the teaching assistant.
"""

import sys
import argparse
from retrieval import RAGRetriever
from llm import OllamaLLM, build_rag_prompt


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print("🎓 RAG-Based Teaching Assistant - Web Development Course")
    print("="*70 + "\n")


def print_results(results, query, response, sources):
    """Pretty print results."""
    print("\n" + "-"*70)
    print(f"Question: {query}")
    print("-"*70 + "\n")
    
    print("📖 Answer:\n")
    print(response)
    
    print("\n" + "-"*70)
    print(sources)
    print("-"*70 + "\n")
    
    print("📊 Relevance Scores:")
    for i, result in enumerate(results, 1):
        score_percent = f"{result['similarity_score']*100:.1f}%"
        print(f"  {i}. {result['title']} (Video {result['number']}): {score_percent}")
    
    print()


def query_assistant(query: str, top_k: int = 5, verbose: bool = False):
    """
    Query the teaching assistant.
    
    Args:
        query: User's question
        top_k: Number of chunks to retrieve
        verbose: Print debug information
    """
    try:
        # Initialize components
        if verbose:
            print("[*] Loading embeddings and retriever...")
        retriever = RAGRetriever()
        
        if verbose:
            print("[*] Initializing LLM...")
        llm = OllamaLLM()
        
        # Retrieve relevant chunks
        if verbose:
            print(f"[*] Retrieving top-{top_k} relevant chunks...")
        results = retriever.retrieve(query, top_k=top_k)
        
        # Build context
        context = retriever.format_context(results)
        
        # Build and execute prompt
        if verbose:
            print("[*] Generating response with LLM...")
        prompt = build_rag_prompt(query, context)
        response = llm.generate(prompt)
        
        # Get source attribution
        sources = retriever.get_source_links(results)
        
        # Display results
        print_results(results, query, response, sources)
        
        return {
            'query': query,
            'response': response,
            'results': results,
            'sources': sources
        }
    
    except FileNotFoundError as e:
        print(f"\n❌ Setup Error: {e}")
        print("\nPlease run setup first:")
        print("  python preprocess_json.py")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        else:
            print("\nRun with --verbose for more details:")
            print("  python rag_assistant.py --query '...' --verbose")
        sys.exit(1)


def check_startup(verbose=False):
    """Check system requirements on startup."""
    import os
    
    # Check for embeddings file (required for all modes)
    if not os.path.exists("embeddings.joblib"):
        print("\n⚠️  ERROR: embeddings.joblib not found!")
        print("\nPlease run the setup first:")
        print("  1. python videos_to_mp3.py")
        print("  2. python mp3_to_json.py")
        print("  3. python preprocess_json.py")
        print()
        sys.exit(1)
    
    if verbose:
        print("[*] System check: embeddings.joblib found ✅")


def print_interactive_startup():
    """Print startup message for interactive mode."""
    print_header()
    print("✅ System ready!")
    print("   - Embeddings: Found")
    print("   - Ollama: Will verify on first query")
    print()
    print("Type your questions below. Press Ctrl+C to exit.\n")


def interactive_mode():
    """Run in interactive mode."""
    print_interactive_startup()
    
    try:
        while True:
            query = input("📝 Your question: ").strip()
            if not query:
                continue
            query_assistant(query)
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋\n")


def main():
    parser = argparse.ArgumentParser(
        description="RAG-based Teaching Assistant for Web Development Course",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rag_assistant.py                          # Interactive mode
  python rag_assistant.py --query "What is HTML?"  # Single query
  python rag_assistant.py -q "CSS basics" -k 3     # Top-3 results
  python rag_assistant.py -q "..." --verbose       # With debug info
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Single query to process (non-interactive mode)"
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=5,
        help="Number of results to retrieve (default: 5)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print debug information"
    )
    
    args = parser.parse_args()
    
    # Verify embeddings exist (required for all modes)
    check_startup(verbose=args.verbose)
    
    if args.query:
        # Single query mode
        print_header()
        query_assistant(args.query, top_k=args.top_k, verbose=args.verbose)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
