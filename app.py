import streamlit as st
import json

from modules.pipeline import run_pipeline
from modules.summarizer import check_ollama_connection, get_available_models
from modules.qa import chat_with_video

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Summarizer Pro",
    page_icon="🎬",
    layout="wide",
)

# ── CSS (FIXED) ─────────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #0B0F19;
    color: #E5E7EB;
}

.block-container {
    padding-top: 1rem;
    max-width: 1100px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1f2937;
}

/* Hero */
.hero {
    text-align: center;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 700;
}

.hero p {
    color: #9CA3AF;
}

/* Input Card */
.input-card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    margin-bottom: 20px;
}

/* Button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 15px;
    border: none;
}

/* Thumbnail */
.thumb img {
    border-radius: 10px;
    transition: 0.3s;
}
.thumb img:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ AI YouTube")

    st.markdown("### 📌 Features")
    st.markdown("- 🎬 Summarizer")
    st.markdown("- 💬 Chat")

    st.markdown("---")

    st.markdown("### ⚙️ Settings")

    model = "gemini-2.5-flash"
    language = st.text_input("Language", "English")

    st.markdown("---")

    if st.button("🎥 Load Demo"):
        with open("demo.json") as f:
            st.session_state.result = json.load(f)
        st.session_state.chat_history = []
        st.success("Demo loaded")

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 AI YouTube Video Summarizer</h1>
    <p>Summarize videos instantly using AI — get insights, key points, and chat with content</p>
</div>
""", unsafe_allow_html=True)

# ── Input Card (FIXED — no empty box) ────────────────────────
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    url = st.text_input("🔗 Paste YouTube link")
    run_btn = st.button("🚀 Generate Summary")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Example Videos (CLICKABLE) ───────────────────────────────
st.markdown("### 📺 Example Videos")

col1, col2, col3 = st.columns(3)

examples = [
    ("aircAruvnKk", "Neural Networks"),
    ("rfscVS0vtbw", "Python Course"),
    ("8hly31xKli0", "Data Structures")
]

for col, (vid, title) in zip([col1, col2, col3], examples):
    thumbnail = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
    link = f"https://www.youtube.com/watch?v={vid}"

    col.markdown(f"""
    <div class="thumb">
        <a href="{link}" target="_blank">
            <img src="{thumbnail}">
        </a>
        <p style="text-align:center; margin-top:8px;">▶️ {title}</p>
    </div>
    """, unsafe_allow_html=True)

# ── Run Pipeline ─────────────────────────────────────────────
if run_btn:
    if not url:
        st.warning("⚠️ Please enter a YouTube URL")
    else:
        with st.spinner("⏳ Processing video..."):
            result = run_pipeline(url, model=model, language=language)
            st.session_state.result = result
            st.session_state.chat_history = []

# ── Display Results ──────────────────────────────────────────
result = st.session_state.result

if result:
    if not result["success"]:
        st.error(result["error"])
    else:
        st.success("✅ Analysis Complete")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Summary",
            "📌 Key Points",
            "🧠 ELI5",
            "⏱️ Timestamps",
            "💬 Chat"
        ])

        with tab1:
            st.write(result["summary"])
            st.write(result["translated_summary"])

        with tab2:
            st.write(result["key_points"])

        with tab3:
            st.write(result["eli5"])

        with tab4:
            for t in result["timestamps"]:
                st.write(f"**{int(t['time'])} sec:** {t['summary']}")

        with tab5:
            with st.form("chat_form"):
                question = st.text_input("Ask a question")
                submit = st.form_submit_button("Ask")

            if submit and question:
                answer = chat_with_video(
                    question,
                    result["rag"]["chunks"],
                    result["rag"]["index"],
                    model,
                    st.session_state.chat_history
                )

                st.session_state.chat_history.append(("You", question))
                st.session_state.chat_history.append(("AI", answer))

            for role, msg in st.session_state.chat_history:
                st.write(f"**{role}:** {msg}")

        with st.expander("📄 Transcript"):
            st.text(result["transcript"]["text"])