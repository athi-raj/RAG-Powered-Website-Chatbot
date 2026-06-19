import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model     = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_chunks(chunks: list[dict]) -> np.ndarray:
    model  = get_model()
    texts  = [c["text"] for c in chunks]
    vecs   = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=64
    )
    return vecs.astype("float32")


def embed_query(query: str) -> np.ndarray:
    model = get_model()
    vec   = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )
    return vec.astype("float32")
