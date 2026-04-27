import requests
from modules.chunker import chunk_text

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:latest"


# ── Connection check ─────────────────────────────────────────
def check_ollama_connection():
    try:
        requests.get("http://localhost:11434")
        return True
    except:
        return False


# ── Get available models ─────────────────────────────────────
def get_available_models():
    try:
        res = requests.get("http://localhost:11434/api/tags")
        data = res.json()
        return [m["name"] for m in data.get("models", [])]
    except:
        return []


# ── Core LLM call ────────────────────────────────────────────
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


# ── Prompt ───────────────────────────────────────────────────
def _summary_prompt(text):
    return f"""
Summarize the following video transcript clearly and concisely:

{text}

Summary:
"""


# ── Main summarization ───────────────────────────────────────
def summarize(text, model=DEFAULT_MODEL):
    chunks = chunk_text(text)

    # If short text
    if len(chunks) == 1:
        return _call_ollama(_summary_prompt(chunks[0]), model)

    # Step 1: summarize each chunk
    partial_summaries = []
    for chunk in chunks:
        s = _call_ollama(_summary_prompt(chunk), model)
        partial_summaries.append(s)

    # Step 2: merge summaries
    combined = "\n\n".join(partial_summaries)

    final_prompt = f"""
You are given partial summaries of a video:

{combined}

Combine them into one clean, concise summary.
"""

    return _call_ollama(final_prompt, model)
