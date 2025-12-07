# 🎧 Whisper Speech-to-Text on Google Colab  
### *(Phase-2 of RAG-Based AI Teaching Assistant)*

This branch documents **Phase-2** of the RAG-Based AI Teaching Assistant project.  
In this stage, we convert lecture audios (`.mp3`) into high-quality text transcripts using **OpenAI Whisper (locally on Google Colab)**.

---

## 🧩 Why This Branch Exists

- In **Phase-1 (main branch)**, raw lecture videos (`.mp4`) were converted to audio (`.mp3`) using `ffmpeg` on local machine.
- But during Phase-2, my **laptop hardware wasn’t powerful enough** to run Whisper efficiently.
- Instead of upgrading hardware or paying for transcription APIs, I used **Google Colab’s free GPU**, which works perfectly for Whisper.
- To keep the repository organized and avoid mixing pipelines, **all Whisper-related code lives in this dedicated branch.**

> 🎯 **Goal of this branch:**  
> Generate structured **JSON transcripts** (with text + timestamps + metadata) from lecture `.mp3` files.

---

## 🏗️ Phase-2 Workflow (This Branch)


---

## 🚀 Step-1: Configure Google Colab Runtime

1. Open the notebook in this branch.
2. Navigate to: **Runtime → Change runtime type**
3. Set:
   - **Runtime type:** Python 3
   - **Hardware accelerator:** **GPU**

> ⚠️ **Do Not Use TPU** — Whisper does not run well on it. GPU works best.

---

## 📦 Step-2: Install Required Libraries (Whisper + Torch + FFmpeg)

Run this cell at the top of your notebook:

```python
!pip install git+https://github.com/openai/whisper.git



