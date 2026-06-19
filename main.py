
import argparse
from src.crawler.crawler import crawl
from src.scraper.scraper import clean_and_chunk
from src.embeddings.embedder import embed_chunks
from src.vectorstore.store import save_index, load_index, index_exists
from src.rag.pipeline import ask

def ingest(url: str):
    if index_exists(url):
        print("✅ Cached index found — skipping crawl.")
        return load_index(url)

    print(f"🌐 Crawling: {url}")
    pages  = crawl(url)

    print(f"🧹 Cleaning & chunking {len(pages)} pages...")
    chunks = clean_and_chunk(pages)

    print(f"🔢 Embedding {len(chunks)} chunks...")
    vectors = embed_chunks(chunks)

    save_index(url, vectors, chunks)
    print("✅ Index saved.")
    return load_index(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",      required=True,  help="Website URL to crawl")
    parser.add_argument("--question", required=False, help="Question to ask")
    args = parser.parse_args()

    ingest(args.url)

    if args.question:
        result = ask(args.url, args.question)
        print(f"\n💬 Answer:\n{result['answer']}")
        print(f"\n📎 Sources:\n" + "\n".join(result["sources"]))
    else:
        print("\n✅ Ingestion complete. Run with --question to query.")
