# RAG-Based AI Teaching Assistant

A Retrieval-Augmented Generation (RAG) system designed to answer course-related questions by retrieving relevant information from lecture content. The system processes lecture videos, converts them into searchable knowledge, and provides context-aware responses with source references.

## Features

* Video-to-text pipeline using Whisper
* Semantic search using vector embeddings
* Retrieval of relevant lecture segments
* Local LLM-powered response generation
* Source attribution with timestamps
* Streamlit-based web interface
* Command-line query interface
* Fully local execution with no paid APIs

---

## System Architecture

```text
Lecture Videos (.mp4)
        ↓
Audio Extraction (.mp3)
        ↓
Whisper Transcription
        ↓
Structured JSON Transcripts
        ↓
Text Chunking
        ↓
BGE-M3 Embeddings
        ↓
Vector Storage (.joblib)
        ↓
Semantic Retrieval
        ↓
Local LLM (DeepSeek-R1)
        ↓
Answer + Source References
```

---

## Technology Stack

| Component      | Technology           |
| -------------- | -------------------- |
| Speech-to-Text | Whisper              |
| Embeddings     | BGE-M3               |
| Vector Search  | Cosine Similarity    |
| LLM            | DeepSeek-R1 (Ollama) |
| Backend        | Python               |
| Interface      | Streamlit / CLI      |

---

## Project Structure

```text
RAG_Based_AI_Teaching_Assistant/
│
├── videos/
├── audios/
├── jsons/
├── retrieval.py
├── llm.py
├── rag_assistant.py
├── streamlit_app.py
├── preprocess_json.py
├── mp3_to_json.py
├── videos_to_mp3.py
├── embeddings.joblib
└── README.md
```

---

## Installation

### 1. Install Dependencies

```bash
pip install -r requirement.txt
```

### 2. Install Ollama

Download and install Ollama.

### 3. Download Required Models

```bash
ollama pull bge-m3
ollama pull deepseek-r1:1.5b
```

---

## Usage

### Generate Knowledge Base

```bash
python videos_to_mp3.py
python mp3_to_json.py
python preprocess_json.py
```

### Launch Web Interface

```bash
streamlit run streamlit_app.py
```

### Launch CLI

```bash
python rag_assistant.py
```

Example:

```bash
python rag_assistant.py --query "What is HTML?"
```

---

## Example Output

Question:

```text
What is overfitting?
```

Response:

```text
Overfitting occurs when a model learns the training data too closely and fails to generalize to unseen data.

Source:
Video 5
Timestamp: 12:34 – 14:10
Similarity Score: 92%
```

---

## Key Highlights

* Fully local execution
* No cloud dependencies
* No paid APIs
* Semantic retrieval with source attribution
* Reusable for multiple courses and lecture collections

---

## Future Enhancements

* Conversational memory
* Multi-course support
* Confidence scoring
* Analytics dashboard
* Voice-based querying

---

## Author

Ritesh Jat

B.Tech, Electronics and Communication Engineering

MANIT Bhopal
