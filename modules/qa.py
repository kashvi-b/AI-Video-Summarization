from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from modules.summarizer import _call_ollama

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store(chunks):
    embeddings = embed_model.encode(chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, embeddings


def query_vector_store(query, chunks, index):
    q_embed = embed_model.encode([query])
    D, I = index.search(np.array(q_embed), k=3)

    return "\n".join([chunks[i] for i in I[0]])


def chat_with_video(question, chunks, index, model_name, history=None):
    # Safety check
    if index is None:
        return "Chat is unavailable for this video."

    context = query_vector_store(question, chunks, index)

    # Include last few messages
    history_text = ""
    if history:
        history_text = "\n".join(
            [f"{role}: {msg}" for role, msg in history[-4:]]
        )

    prompt = f"""
You are an AI assistant helping understand a video.

Previous conversation:
{history_text}

Relevant context from the video:
{context}

Answer the user's question clearly.

Question: {question}
"""

    return _call_ollama(prompt, model_name)