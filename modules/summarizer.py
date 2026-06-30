import streamlit as st
import google.generativeai as genai
from modules.chunker import chunk_text

# Configure Gemini once
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

DEFAULT_MODEL = "gemini-2.5-flash"

# Create model once
gemini_model = genai.GenerativeModel(DEFAULT_MODEL)


def _call_gemini(prompt, model=DEFAULT_MODEL):
    response = gemini_model.generate_content(prompt)
    return response.text


def summarize(text, model=DEFAULT_MODEL):
    chunks = chunk_text(text)

    if len(chunks) == 1:
        return _call_gemini(
            f"Summarize the following text clearly:\n\n{text}",
            model
        )

    partial_summaries = []

    for chunk in chunks:
        summary = _call_gemini(
            f"Summarize:\n\n{chunk}",
            model
        )
        partial_summaries.append(summary)

    combined = "\n\n".join(partial_summaries)

    final_summary = _call_gemini(
        f"Combine these summaries into one concise summary:\n\n{combined}",
        model
    )

    return final_summary


def get_key_points(text, model=DEFAULT_MODEL):
    prompt = f"""
Extract 5–8 important key points from this video transcript:

{text}

Return only bullet points.
"""
    return _call_gemini(prompt, model)


def explain_simple(text, model=DEFAULT_MODEL):
    prompt = f"""
Explain this in a very simple way (like I'm 5 years old):

{text}

Use short sentences and simple words.
"""
    return _call_gemini(prompt, model)