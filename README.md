# 🎬 AI Video Summarizer Pro

AI-powered YouTube video summarizer built using **local LLMs (Ollama)**.
It extracts video transcripts and generates summaries, key insights, and interactive Q&A — all running **100% locally (no paid APIs)**.

---

## 🚀 Features

* 📋 **Video Summary** – Concise overview of video content
* 📌 **Key Points Extraction** – Important highlights in bullet form
* 🧠 **Explain Like I’m 5 (ELI5)** – Simplified explanation
* ⏱️ **Timestamp Summaries** – Segment-wise insights
* 💬 **Chat with Video (RAG)** – Ask questions about video content
* 🌍 **Multi-language Output** – Translate summaries to any language
* ⚡ **Runs Locally** – Powered by Ollama (no API cost)

---

## 🛠 Tech Stack

* **Python**
* **Streamlit** (UI)
* **Ollama (llama3)** – Local LLM
* **FAISS** – Vector search (RAG)
* **Sentence Transformers** – Embeddings
* **youtube-transcript-api** – Transcript extraction

---

## 📂 Project Structure

```
ai-video/
│
├── app.py
├── modules/
│   ├── pipeline.py
│   ├── summarizer.py
│   ├── transcript.py
│   ├── qa.py
│   ├── chunker.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/kashvi-b/Ai-Video-Summarization.git
cd Ai-Video-Summarization
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install and run Ollama

Download from: https://ollama.com

Then run:

```bash
ollama pull llama3
ollama serve
```

---

### 4. Run the app

```bash
streamlit run app.py
```

---

## ▶️ Usage

1. Paste a YouTube video link
2. Click **Analyze Video**
3. View:

   * Summary
   * Key Points
   * ELI5 Explanation
   * Timestamp Insights
4. Ask questions in **Chat tab**

---

## ⚠️ Limitations

This project uses `youtube-transcript-api` to fetch captions.

Due to YouTube restrictions:

* Some videos **do not allow transcript access**
* Some transcripts are **blocked by YouTube**
* Some videos **have no captions available**

👉 In such cases, the app will show an error message.
👉 This is expected behavior and not a bug.

---

## 🔮 Future Improvements

* 🎤 Whisper integration (speech-to-text fallback)
* 📄 Download summary as PDF
* 💬 Chat memory (conversation history)
* 🚀 Deployment (Streamlit Cloud / Render)

---

## 👩‍💻 Author

**Kashvi Bhardwaj**
Computer Science Student @ SRM IST

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
