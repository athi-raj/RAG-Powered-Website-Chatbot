
import os
from openai import OpenAI
from src.embeddings.embedder import embed_query
from src.vectorstore.store   import load_index, search, index_exists
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant. Answer questions using ONLY
the website content provided below. If the answer isn't in the context,
say: "I couldn't find that information on this website."
Never make up information."""


def build_context(chunks: list[dict]) -> str:
    return "\n\n---\n\n".join(
        f"[Page: {c['title']}]\n[URL: {c['source_url']}]\n{c['text']}"
        for c in chunks
    )


def ask(url: str, question: str) -> dict:
    if not index_exists(url):
        return {"answer": "Website not indexed yet. Please ingest first.",
                "sources": []}

    index, chunks = load_index(url)
    query_vec     = embed_query(question)
    top_chunks    = search(index, chunks, query_vec, top_k=4)
    context       = build_context(top_chunks)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        max_tokens=1000,
        temperature=0.2
    )

    answer  = response.choices[0].message.content.strip()
    sources = list({c["source_url"] for c in top_chunks})
    return {"answer": answer, "sources": sources}
