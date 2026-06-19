import re
import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
RAW_DIR       = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(RAW_DIR,       exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""]
)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+",           " ",    text)
    text = re.sub(r"[^\x20-\x7E]", "",     text)
    text = re.sub(r"([.!?])\1+",   r"\1",  text)
    return text.strip()


def save_raw(pages: list[dict]):
    for page in pages:
        fname = re.sub(r"[^\w]", "_", page["url"])[:80] + ".json"
        with open(os.path.join(RAW_DIR, fname), "w") as f:
            json.dump(page, f, indent=2)


def clean_and_chunk(pages: list[dict]) -> list[dict]:
    save_raw(pages)
    chunks = []

    for page in pages:
        text   = clean_text(page["text"])
        splits = splitter.split_text(text)

        for i, chunk_text in enumerate(splits):
            if len(chunk_text.strip()) < 40:
                continue
            chunk = {
                "text":       chunk_text,
                "source_url": page["url"],
                "title":      page["title"],
                "chunk_idx":  i
            }
            chunks.append(chunk)

    # Save processed chunks
    with open(os.path.join(PROCESSED_DIR, "chunks.json"), "w") as f:
        json.dump(chunks, f, indent=2)

    return chunks
