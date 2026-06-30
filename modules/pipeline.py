import streamlit as st

from modules.transcript import get_transcript
from modules.whisper_fallback import get_transcript_whisper
from modules.summarizer import (
    summarize,
    get_key_points,
    explain_simple,
    _call_gemini
)
from modules.chunker import chunk_text
from modules.qa import build_vector_store


# ── CACHED FUNCTIONS ─────────────────────────────────────────

@st.cache_data(show_spinner=False)
def cached_transcript(url, language):
    try:
        return get_transcript(url, language=language)
    except Exception:
        return get_transcript_whisper(url)


@st.cache_data(show_spinner=False)
def cached_summary(text, model):
    return summarize(text, model=model)


# ── MAIN PIPELINE ────────────────────────────────────────────

def run_pipeline(url, model, language):
    try:
        # ── Step 1: Transcript (with fallback) ───────────────
        transcript_data = cached_transcript(url, language)

        text = transcript_data["text"]
        segments = transcript_data["segments"]

        # ── Step 2: Chunking ───────────────────────────────
        chunks = chunk_text(text)

        # ── Step 3: LLM outputs ────────────────────────────
        summary = cached_summary(text, model)
        key_points = get_key_points(text, model)
        eli5 = explain_simple(text, model)

        # ── Step 4: Timestamp summaries ────────────────────
        timestamp_summaries = []
        for seg in segments[:10]:
            seg_summary = summarize(seg["text"], model=model)

            timestamp_summaries.append({
                "time": seg["start"],
                "summary": seg_summary
            })

        # ── Step 5: RAG setup ─────────────────────────────
        try:
            index, _ = build_vector_store(chunks)
        except Exception:
            index = None

        # ── Step 6: Translation ───────────────────────────
        translated_summary = _call_gemini(
            f"Translate this summary to {language}:\n\n{summary}",
            model
        )

        # ── Step 7: Return ────────────────────────────────
        return {
            "success": True,
            "summary": summary,
            "key_points": key_points,
            "eli5": eli5,
            "translated_summary": translated_summary,
            "timestamps": timestamp_summaries,
            "rag": {
                "chunks": chunks,
                "index": index
            },
            "transcript": {
                "text": text,
                "segments": segments
            },
            "chunks": {
                "text_chunks": chunks,
                "token_count": len(text)
            }
        }

    except Exception as e:
        print("Pipeline error:", e)

        return {
            "success": False,
            "error": (
                "❌ Could not process this video.\n\n"
                "Try another video or use demo mode."
            )
        }