from modules.transcript import get_transcript
from modules.summarizer import (
    summarize,
    get_key_points,
    explain_simple,
    _call_ollama
)
from modules.chunker import chunk_text
from modules.qa import build_vector_store


def run_pipeline(url, model, language):
    """
    Full pipeline:
    - Transcript
    - Summary
    - Key points
    - ELI5
    - Timestamps
    - RAG setup
    - Translation
    """

    try:
        # ── Step 1: Get transcript ───────────────────────────
        transcript_data = get_transcript(url, language=language)

        text = transcript_data["text"]
        segments = transcript_data["segments"]

        # ── Step 2: Chunking ─────────────────────────────────
        chunks = chunk_text(text)

        # ── Step 3: LLM outputs ─────────────────────────────
        summary = summarize(text, model=model)
        key_points = get_key_points(text, model=model)
        eli5 = explain_simple(text, model=model)

        # ── Step 4: Timestamp summaries (limited for speed) ─
        timestamp_summaries = []
        for seg in segments[:10]:  # limit for performance
            t = seg["start"]
            text_seg = seg["text"]

            seg_summary = summarize(text_seg, model=model)

            timestamp_summaries.append({
                "time": t,
                "summary": seg_summary
            })

        # ── Step 5: RAG setup (store only chunks, rebuild index later) ─
        try:
            index, _ = build_vector_store(chunks)
        except Exception:
            index = None  # fail-safe

        # ── Step 6: Multi-language summary ──────────────────
        translated_summary = _call_ollama(
            f"Translate this summary to {language}:\n\n{summary}",
            model
        )

        # ── Step 7: Return everything ───────────────────────
        return {
            "success": True,

            "summary": summary,
            "key_points": key_points,
            "eli5": eli5,

            "translated_summary": translated_summary,

            "timestamps": timestamp_summaries,

            "rag": {
                "chunks": chunks,
                "index": index  # may be None (safe)
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
        print("Pipeline error:", e)  # debug log

        return {
            "success": False,
            "error": (
                "❌ Transcript not accessible for this video.\n\n"
                "Possible reasons:\n"
                "- Captions are disabled\n"
                "- YouTube blocked transcript access\n"
                "- Video has restricted subtitles\n\n"
                "👉 Try another video."
            )
        }