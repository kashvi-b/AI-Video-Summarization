import streamlit as st
import json

from modules.pipeline import run_pipeline
from modules.summarizer import check_ollama_connection, get_available_models
from modules.qa import chat_with_video

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Summarizer Pro",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI Video Summarizer Pro")
st.caption("Powered by Ollama + RAG")

# ── Check Ollama ─────────────────────────────────────────────
if not check_ollama_connection():
    st.error("⚠️ Ollama is not running. Run: `ollama serve`")
    st.stop()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    models = get_available_models()

    if not models:
        st.error("❌ No models found. Run: `ollama pull llama3`")
        st.stop()

    display_models = [m.split(":")[0] for m in models]
    model_map = dict(zip(display_models, models))

    selected_display = st.selectbox("🤖 Model", display_models)
    model = model_map[selected_display]

    language = st.text_input("🌍 Output Language", value="English")

    st.markdown("---")
    st.markdown("Paste a YouTube link or use demo mode")

# ── Demo Button (IMPORTANT) ───────────────────────────────────
if st.button("🎥 Load Demo (Guaranteed Working)"):
    with open("demo.json") as f:
        st.session_state.result = json.load(f)
    st.success("✅ Demo Loaded")

# ── Input ────────────────────────────────────────────────────
url = st.text_input("🔗 Enter YouTube URL")

run_btn = st.button("🚀 Analyze Video", use_container_width=True)

# ── Session state ─────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Run pipeline ──────────────────────────────────────────────
if run_btn:
    if not url:
        st.warning("⚠️ Please enter a YouTube URL")
    else:
        with st.spinner("⏳ Processing... This may take a few seconds"):
            result = run_pipeline(url, model=model, language=language)
            st.session_state.result = result
            st.session_state.chat_history = []  # reset chat on new video

# ── Display results ───────────────────────────────────────────
result = st.session_state.result

if result:
    # ❌ Failure
    if not result["success"]:
        st.error(result["error"])

    # ✅ Success
    else:
        st.success("✅ Analysis Complete")

        st.info(f"🧩 Chunks: {len(result['chunks']['text_chunks'])}")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Summary",
            "📌 Key Points",
            "🧠 ELI5",
            "⏱️ Timestamps",
            "💬 Chat"
        ])

        # ── Summary ───────────────────────────────────────
        with tab1:
            st.subheader("📋 Summary")
            st.write(result["summary"])

            st.subheader("🌍 Translated Summary")
            st.write(result["translated_summary"])

        # ── Key Points ────────────────────────────────────
        with tab2:
            st.subheader("📌 Key Points")
            st.write(result["key_points"])

        # ── ELI5 ──────────────────────────────────────────
        with tab3:
            st.subheader("🧠 Explain Like I'm 5")
            st.write(result["eli5"])

        # ── Timestamps ───────────────────────────────────
        with tab4:
            st.subheader("⏱️ Timestamp Summaries")
            for t in result["timestamps"]:
                st.write(f"**{int(t['time'])} sec:** {t['summary']}")

        # ── Chat with memory ─────────────────────────────
        with tab5:
            st.subheader("💬 Chat with Video")

            with st.form("chat_form"):
                question = st.text_input("Ask a question about the video")
                submit = st.form_submit_button("Ask")

            if submit:
                if not question:
                    st.warning("Please enter a question")

                elif result["rag"]["index"] is None:
                    st.info("Demo mode: Chat disabled")

                else:
                    answer = chat_with_video(
                        question,
                        result["rag"]["chunks"],
                        result["rag"]["index"],
                        model
                    )

                    st.session_state.chat_history.append(("You", question))
                    st.session_state.chat_history.append(("AI", answer))

            # Display chat history
            for role, msg in st.session_state.chat_history:
                if role == "You":
                    st.markdown(f"**🧑 You:** {msg}")
                else:
                    st.markdown(f"**🤖 AI:** {msg}")

        # ── Transcript ────────────────────────────────────
        with st.expander("📄 View Full Transcript"):
            st.text(result["transcript"]["text"])