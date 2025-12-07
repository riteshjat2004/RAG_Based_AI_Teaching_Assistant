# RAG-Based AI Teaching Assistant (Data Science Edition)

This repository documents the development of a Retrieval-Augmented Generation (RAG) based Teaching Assistant designed for Data Science learners. The objective of this project is to create an assistant capable of answering course-related questions by retrieving and interpreting relevant information from actual lecture content.  

The workflow mimics how a real teaching assistant learns: it first understands the lecture material and then uses that knowledge to respond accurately and contextually.

---

## Phase 1: Converting Raw Lecture Videos into Usable Text

The project begins with collecting lecture material in `.mp4` video format. Because language models cannot directly process video, the content must be converted to a text-readable form. This phase focuses on transforming video data into structured textual knowledge.

### Processing Workflow

| Stage | Task | Tool/Method |
|-------|------|-------------|
| 1 | Convert `.mp4` videos to `.mp3` audio | FFmpeg |
| 2 | Generate text transcripts from audio | Whisper (speech-to-text) |
| 3 | Clean, structure and store transcripts | Python preprocessing |

### Why Audio Conversion?

Transcribing audio is significantly more efficient than transcribing video. Extracting audio first reduces processing cost and improves transcription performance, especially when working with cloud or local resources.

---

## About Transcription in Phase 2

Although Whisper was chosen for transcription, local hardware limitations prevented smooth execution of the speech-to-text model on the primary development machine.  
Therefore:

- The transcription stage was moved to a dedicated branch.
- Google Colab GPUs were used to run Whisper efficiently.
- The transcripts were exported in structured JSON format, including timestamps and text segments.
- Only JSON outputs were brought back for further RAG processing in later phases.

These outputs serve as the textual knowledge base for the Teaching Assistant.

---

## Project Files (Current Status)


---

### Next Steps

Subsequent phases will focus on:

- Splitting transcripts into context-aware chunks
- Generating embeddings using a vector store
- Building the query answering pipeline using RAG-based retrieval
- Deploying an interactive user interface

Progress from the transcription branch will be integrated into the main branch in later stages.

---

If you would like, I can now prepare:

- A `PHASE_3_README.md` describing chunking and embeddings  
- A proposed folder restructuring for scalability  
- Documentation for merging branch outputs into the core pipeline

Let me know your preference.
