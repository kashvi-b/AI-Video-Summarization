from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from modules.summarizer import _call_ollama

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store(chunks):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, embeddings


def query_vector_store(query, chunks, index):
    q_embed = model.encode([query])
    D, I = index.search(np.array(q_embed), k=3)

    context = "\n".join([chunks[i] for i in I[0]])

    return context


def chat_with_video(question, chunks, index, model_name):
    context = query_vector_store(question, chunks, index)

    prompt = f"""
Answer the question based only on this context:

{context}

Question: {question}
"""

    return _call_ollama(prompt, model_name)