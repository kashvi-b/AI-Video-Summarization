import tiktoken

def get_token_count(text: str, model: str = "gpt2") -> int:
    """Count tokens using tiktoken."""
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(text))


def clean_text(text: str) -> str:
    """Remove filler words, fix spacing, strip junk."""
    import re
    text = re.sub(r"\[.*?\]", "", text)        # remove [Music], [Applause] etc.
    text = re.sub(r"\s+", " ", text)           # collapse whitespace
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)  # fix broken words
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into token-aware overlapping chunks.
    chunk_size: max tokens per chunk
    overlap: tokens shared between consecutive chunks
    """
    enc = tiktoken.get_encoding("gpt2")
    tokens = enc.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))
        start += chunk_size - overlap  # slide with overlap

    return chunks


def chunk_segments_by_time(segments: list[dict], window_seconds: int = 120) -> list[dict]:
    """
    Group transcript segments into time-window chunks.
    Returns: [{ "start": float, "end": float, "text": str }]
    Used for timestamp-based summaries (Step 7).
    """
    if not segments:
        return []

    grouped = []
    current_group = []
    window_start = segments[0]["start"]

    for seg in segments:
        current_group.append(seg)
        elapsed = seg["start"] - window_start

        if elapsed >= window_seconds:
            grouped.append({
                "start": window_start,
                "end": seg["start"] + seg.get("duration", 0),
                "text": clean_text(" ".join(s["text"] for s in current_group)),
            })
            current_group = []
            window_start = seg["start"]

    # catch leftover segments
    if current_group:
        grouped.append({
            "start": window_start,
            "end": current_group[-1]["start"] + current_group[-1].get("duration", 0),
            "text": clean_text(" ".join(s["text"] for s in current_group)),
        })

    return grouped


def prepare_chunks(raw_text: str, segments: list[dict]) -> dict:
    """
    Master function — returns everything downstream modules need.
    """
    cleaned = clean_text(raw_text)
    return {
        "cleaned_text": cleaned,
        "token_count": get_token_count(cleaned),
        "text_chunks": chunk_text(cleaned),
        "timed_chunks": chunk_segments_by_time(segments),
    }