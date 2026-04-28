from modules.transcript import get_transcript
from modules.summarizer import summarize, get_key_points, explain_simple


def run_pipeline(url, model, language):
    try:
        transcript_data = get_transcript(url, language=language)

        text = transcript_data["text"]
        segments = transcript_data["segments"]

        # ── LLM outputs ─────────────────────────
        summary = summarize(text, model=model)
        key_points = get_key_points(text, model=model)
        eli5 = explain_simple(text, model=model)

        return {
            "success": True,
            "summary": summary,
            "key_points": key_points,
            "eli5": eli5,
            "transcript": {
                "text": text,
                "segments": segments
            },
            "chunks": {
                "text_chunks": [text],
                "token_count": len(text)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }