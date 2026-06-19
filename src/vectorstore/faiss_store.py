import faiss
import pickle
import hashlib
import os
import numpy as np

INDEX_DIR = "data/vectorstore"
os.makedirs(INDEX_DIR, exist_ok=True)


def _paths(url: str) -> tuple[str, str]:
    h = hashlib.md5(url.encode()).hexdigest()[:12]
    return (
        os.path.join(INDEX_DIR, f"{h}.faiss"),
        os.path.join(INDEX_DIR, f"{h}.pkl")
    )


def index_exists(url: str) -> bool:
    idx, _ = _paths(url)
    return os.path.exists(idx)


def save_index(url: str, vectors: np.ndarray, chunks: list[dict]):
    dim   = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    idx_path, meta_path = _paths(url)
    faiss.write_index(index, idx_path)
    with open(meta_path, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Index saved: {idx_path}")


def load_index(url: str) -> tuple[faiss.Index, list[dict]]:
    idx_path, meta_path = _paths(url)
    index  = faiss.read_index(idx_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def search(index: faiss.Index, chunks: list[dict],
           query_vec: np.ndarray, top_k: int = 4) -> list[dict]:
    scores, ids = index.search(query_vec, top_k)
    results = []
    for score, i in zip(scores[0], ids[0]):
        if i < 0:
            continue
        results.append({**chunks[i], "score": round(float(score), 4)})
    return results
