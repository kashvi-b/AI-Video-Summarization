from modules.transcript import get_transcript
from modules.summarizer import summarize


def run_pipeline(url, model, language):
    """
    Main pipeline:
    1. Get transcript
    2. Summarize text
    3. Return structured result
    """

    try:
        # ── Step 1: Get transcript ───────────────────────────
        transcript_data = get_transcript(url, language=language)

        text = transcript_data["text"]
        segments = transcript_data["segments"]

        # ── Step 2: Summarize ───────────────────────────────
        summary = summarize(text, model=model)

        # ── Step 3: Return result ───────────────────────────
        return {
            "success": True,
            "summary": summary,
            "transcript": {
                "text": text,
                "segments": segments
            },
            "chunks": {
                "text_chunks": [text],  # simple for now
                "token_count": len(text)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }