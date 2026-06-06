"""
Streamlit UI for RAG-based Teaching Assistant.
Provides a web-based interface for the teaching assistant.
"""

import streamlit as st
from retrieval import RAGRetriever
from llm import OllamaLLM, build_rag_prompt
import time


# Page configuration
st.set_page_config(
    page_title="RAG Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .result-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .source-badge {
        display: inline-block;
        background-color: #e8f4f8;
        padding: 5px 10px;
        border-radius: 3px;
        margin: 5px 5px 5px 0;
        font-size: 0.85em;
    }
    .relevance-high {
        color: #28a745;
    }
    .relevance-medium {
        color: #ffc107;
    }
    .relevance-low {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_retriever():
    """Load retriever with caching."""
    try:
        return RAGRetriever()
    except FileNotFoundError as e:
        st.error(f"❌ Error: {e}")
        st.stop()


@st.cache_resource
def load_llm():
    """Load LLM with caching."""
    return OllamaLLM()


def relevance_color(score):
    """Determine color based on relevance score."""
    if score > 0.7:
        return "relevance-high"
    elif score > 0.4:
        return "relevance-medium"
    else:
        return "relevance-low"


def format_timestamp(start, end):
    """Format seconds to MM:SS."""
    def sec_to_mmss(sec):
        minutes = int(sec // 60)
        seconds = int(sec % 60)
        return f"{minutes}:{seconds:02d}"
    return f"{sec_to_mmss(start)} - {sec_to_mmss(end)}"


def main():
    # Header
    st.title("🎓 RAG-Based Teaching Assistant")
    st.markdown("Web Development Course - Powered by Local AI")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        top_k = st.slider(
            "Number of results to retrieve",
            min_value=1,
            max_value=10,
            value=5,
            help="How many relevant chunks to retrieve for each query"
        )
        
        temperature = st.slider(
            "Response creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower = more focused, Higher = more creative"
        )
        
        st.divider()
        st.subheader("📊 About")
        st.info(
            "This is a Retrieval-Augmented Generation (RAG) teaching assistant "
            "for the Web Development course. It retrieves relevant lecture content "
            "and generates contextual answers using local AI models."
        )
        
        st.divider()
        st.subheader("🔧 Troubleshooting")
        if st.button("Check Service Status"):
            try:
                retriever = load_retriever()
                llm = load_llm()
                st.success("✅ All services running!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Ask a Question")
        query = st.text_area(
            "Enter your question about the course:",
            placeholder="e.g., What is HTML? How do I create a form? What are CSS selectors?",
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        st.subheader("Quick Actions")
        process_button = st.button("🔍 Get Answer", use_container_width=True)
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    # Process query
    if process_button and query.strip():
        try:
            with st.spinner("🤔 Thinking..."):
                retriever = load_retriever()
                llm = load_llm()
                
                # Retrieve
                st.write("📚 Retrieving relevant content...")
                results = retriever.retrieve(query, top_k=top_k)
                
                # Build context and generate
                st.write("📝 Generating answer...")
                context = retriever.format_context(results)
                prompt = build_rag_prompt(query, context)
                response = llm.generate(prompt, temperature=temperature)
            
            # Display response
            st.success("✅ Answer generated!")
            st.divider()
            
            st.subheader("🤖 Answer")
            st.write(response)
            
            st.divider()
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["📖 Retrieved Chunks", "📍 Sources", "📊 Metadata"])
            
            with tab1:
                st.subheader("Retrieved Relevant Chunks")
                for i, result in enumerate(results, 1):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"### {i}. {result['title']} (Video {result['number']})")
                            st.caption(f"Timestamp: {format_timestamp(result['start'], result['end'])}")
                        with col2:
                            score_percent = f"{result['similarity_score']*100:.1f}%"
                            score_class = relevance_color(result['similarity_score'])
                            st.markdown(
                                f"<p class='{score_class}'><strong>{score_percent}</strong></p>",
                                unsafe_allow_html=True
                            )
                        
                        st.write(result['text'])
                        st.divider()
            
            with tab2:
                st.subheader("📚 Source References")
                for result in results:
                    timestamp = format_timestamp(result['start'], result['end'])
                    st.markdown(
                        f"<div class='source-badge'>"
                        f"<strong>{result['title']}</strong> (Video {result['number']}) @ {timestamp}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            
            with tab3:
                st.subheader("📊 Retrieval Metadata")
                metadata_df = {
                    'Chunk': [r['chunk_id'] for r in results],
                    'Video': [r['title'] for r in results],
                    'Number': [r['number'] for r in results],
                    'Relevance': [f"{r['similarity_score']:.2%}" for r in results],
                    'Duration': [
                        f"{format_timestamp(r['start'], r['end'])}" 
                        for r in results
                    ]
                }
                st.dataframe(metadata_df, use_container_width=True)
            
            # Export option
            st.divider()
            st.subheader("💾 Export")
            export_text = f"""QUESTION:
{query}

ANSWER:
{response}

SOURCES:
"""
            for result in results:
                export_text += f"\n- {result['title']} (Video {result['number']}) @ {format_timestamp(result['start'], result['end'])}"
            
            st.download_button(
                label="📥 Download Answer as Text",
                data=export_text,
                file_name="rag_answer.txt",
                mime="text/plain"
            )
        
        except ConnectionError as e:
            st.error(f"❌ Connection Error: {e}")
            st.info("💡 Make sure Ollama is running: `ollama serve`")
        except FileNotFoundError as e:
            st.error(f"❌ Missing File: {e}")
            st.info("💡 Generate embeddings first: `python preprocess_json.py`")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Check the console for detailed error information.")
    
    elif clear_button:
        st.rerun()


if __name__ == "__main__":
    main()
