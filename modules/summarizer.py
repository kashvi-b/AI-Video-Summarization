import requests
from modules.chunker import chunk_text

# ── Config ─────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:latest"


# ── Connection check ───────────────────────────────────
def check_ollama_connection():
    try:
        requests.get("http://localhost:11434")
        return True
    except:
        return False


# ── Get available models ───────────────────────────────
def get_available_models():
    try:
        res = requests.get("http://localhost:11434/api/tags")
        data = res.json()
        return [m["name"] for m in data.get("models", [])]
    except:
        return []


# ── Core LLM call ──────────────────────────────────────
def _call_ollama(prompt, model=DEFAULT_MODEL):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "")


# ── Summary ────────────────────────────────────────────
def summarize(text, model=DEFAULT_MODEL):
    chunks = chunk_text(text)

    # If short text
    if len(chunks) == 1:
        return _call_ollama(
            f"Summarize the following text clearly:\n\n{text}",
            model
        )

    # Step 1: summarize each chunk
    partial_summaries = []
    for chunk in chunks:
        summary = _call_ollama(
            f"Summarize:\n\n{chunk}",
            model
        )
        partial_summaries.append(summary)

    # Step 2: merge summaries
    combined = "\n\n".join(partial_summaries)

    final_summary = _call_ollama(
        f"Combine these summaries into one concise summary:\n\n{combined}",
        model
    )

    return final_summary


# ── Key Points ─────────────────────────────────────────
def get_key_points(text, model=DEFAULT_MODEL):
    prompt = f"""
Extract 5–8 important key points from this video transcript:

{text}

Return only bullet points.
"""
    return _call_ollama(prompt, model)


# ── Explain Like I'm 5 ─────────────────────────────────
def explain_simple(text, model=DEFAULT_MODEL):
    prompt = f"""
Explain this in a very simple way (like I'm 5 years old):

{text}

Use short sentences and simple words.
"""
    return _call_ollama(prompt, model)
