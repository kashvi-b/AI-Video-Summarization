# 🎬 AI Video Summarizer Pro

A modern AI-powered application that summarizes YouTube videos, extracts key insights, and allows users to chat with video content — all running locally using Ollama.

---

## 🚀 Features

### 🎯 Core Features

* 📋 **Video Summarization** – Generate concise summaries from YouTube videos
* 📌 **Key Points Extraction** – Important highlights in bullet form
* 🧠 **Explain Like I’m 5 (ELI5)** – Simplified explanation of complex content
* ⏱️ **Timestamp Summaries** – Section-wise breakdown of the video
* 💬 **Chat with Video (RAG)** – Ask questions about the video using semantic search

---

### ⚡ Advanced Features

* 🎤 **Whisper Fallback** – Works even if YouTube captions are unavailable
* 🌍 **Multi-language Output** – Translate summaries into different languages
* 🧠 **Local LLM (Ollama)** – 100% free and private processing
* 📦 **Vector Search (FAISS)** – Fast retrieval for Q&A
* ⚡ **Caching for Performance** – Faster repeated runs

---

### 🎨 UI/UX Highlights

* ✨ Premium dark-themed interface
* 🎬 Hero section + input card design
* 📺 Clickable example video thumbnails
* 🎯 Gradient CTA buttons
* 📊 Clean layout with tabs and sections

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM**: Ollama (Llama3 / Mistral)
* **Speech-to-Text**: OpenAI Whisper
* **Vector DB**: FAISS
* **Embeddings**: Sentence Transformers
* **Data Source**: YouTube Transcript API

---

## 📦 Installation

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

### 3. Install Ollama

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

## 🎥 Demo

👉 Use built-in **Demo Mode** or try these videos:

* https://www.youtube.com/watch?v=aircAruvnKk
* https://www.youtube.com/watch?v=rfscVS0vtbw

---

## ⚠️ Known Limitations

* Some videos may not provide transcripts due to:

  * Captions disabled
  * Region restrictions
  * YouTube blocking requests

* Whisper fallback may:

  * Be slower for long videos
  * Use more CPU

---

## 💡 How It Works

1. Extract transcript from YouTube
2. If unavailable → use Whisper fallback
3. Split transcript into chunks
4. Generate:

   * Summary
   * Key Points
   * ELI5
5. Store embeddings using FAISS
6. Enable chat via RAG

---

## 📌 Future Improvements

* 📄 Export summary as PDF
* 🎬 Embedded video player
* 📊 Real-time progress tracking
* 🌐 Deploy on cloud (Streamlit / Vercel backend)

---

## 🤝 Contributing

Pull requests are welcome!
Feel free to open issues for bugs or feature requests.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👩‍💻 Author

**Kashvi Bhardwaj**

---

⭐ If you like this project, consider giving it a star on GitHub!

