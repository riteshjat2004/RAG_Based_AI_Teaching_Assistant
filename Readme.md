# 🎓 RAG-Based AI Teaching Assistant (Data Science Edition)

> **Learn Smarter. Ask Anything. Get Context-Aware Answers.**

Welcome to our mini journey of building a **RAG (Retrieval-Augmented Generation) powered Teaching Assistant** for **Data Science learners**.  
The goal is simple:  
💡 **You ask a question related to your course → The AI searches through course material → It gives the correct answer with context.**

Just like asking a real TA during class… except this one never gets annoyed 😄

---

## 🔰 Phase-1: Getting Started (From Raw Videos → Useful Text)

Before a Teaching Assistant can teach, it needs to “study” the course material.  
In this project, we start with **raw lecture videos** (in `.mp4` format).  
Since videos cannot be directly processed by a text-based LLM, we first convert them into **textual knowledge** through these steps:

### 🎥 ➝ 🔊 ➝ 📄 Workflow
| Step | Action | Tech Used |
|------|--------|-----------|
| 1 | Convert `.mp4` lecture videos to `.mp3` | `ffmpeg` |
| 2 | Transcribe audio into text | `Whisper AI` |
| 3 | Clean & store text data | Python, pre-processing |

📌 **Why convert to audio first?**  
Because it reduces processing load and speeds up transcription by Whisper.

📌 **Good News!**  
You can use **any course videos you want**. This repo only shows the pipeline.  
👉 *You can plug in your **own lectures** and build your personal AI TA!*

---

## 📁 Project Files (So Far)

