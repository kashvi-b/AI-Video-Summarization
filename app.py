import streamlit as st
from modules.pipeline import run_pipeline
from modules.summarizer import check_ollama_connection, get_available_models

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Summarizer Pro",
    page_icon="🎬",
    layout="wide",
)

# ── Title ────────────────────────────────────────────────────
st.title("🎬 AI Video Summarizer Pro")
st.caption("Powered by Ollama — 100% free & local")

# ── Check Ollama ─────────────────────────────────────────────
if not check_ollama_connection():
    st.error("⚠️ Ollama is not running.\n\nRun:\n\n`ollama serve`")
    st.stop()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    models = get_available_models()

    if not models:
        st.error("❌ No models found.\n\nRun:\n\n`ollama pull llama3`")
        st.stop()

    # Clean display (remove :latest)
    display_models = [m.split(":")[0] for m in models]
    model_map = dict(zip(display_models, models))

    selected_display = st.selectbox("🤖 Model", display_models)
    model = model_map[selected_display]

    language = st.text_input("🌐 Transcript Language", value="en")

    st.markdown("---")
    st.markdown("### ℹ️ Instructions")
    st.markdown("""
    1. Paste a YouTube link  
    2. Click **Analyze Video**  
    3. Wait for results  
    """)

# ── Input ────────────────────────────────────────────────────
url = st.text_input(
    "🔗 Enter YouTube URL",
    placeholder="https://youtube.com/watch?v=..."
)

run_btn = st.button("🚀 Analyze Video", use_container_width=True)

# ── Session state ─────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ── Run pipeline ──────────────────────────────────────────────
if run_btn:
    if not url:
        st.warning("⚠️ Please enter a YouTube URL")
    else:
        with st.spinner("⏳ Processing video..."):
            result = run_pipeline(url, model=model, language=language)
            st.session_state.result = result

# ── Display results ───────────────────────────────────────────
result = st.session_state.result

if result:
    if not result["success"]:
        st.error(f"❌ {result['error']}")
    else:
        # Metrics
        col1, col2 = st.columns(2)
        col1.metric("🧩 Chunks", len(result["chunks"]["text_chunks"]))
        col2.metric("⏱️ Segments", len(result["transcript"]["segments"]))

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3 = st.tabs([
            "📋 Summary",
            "⏱️ Timestamps",
            "💬 Chat"
        ])

        # ── Summary ───────────────────────────────────────────
        with tab1:
            st.subheader("📋 Summary")
            st.write(result["summary"])

        # ── Timestamps ────────────────────────────────────────
        with tab2:
            st.subheader("⏱️ Timestamp Summaries")
            st.info("Coming soon...")

        # ── Chat ──────────────────────────────────────────────
        with tab3:
            st.subheader("💬 Chat with Video")
            st.info("Coming soon...")

        # ── Transcript ────────────────────────────────────────
        with st.expander("📄 View Raw Transcript"):
            st.text(result["transcript"]["text"])