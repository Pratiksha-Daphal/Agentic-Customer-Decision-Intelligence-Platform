import faiss
import pickle
from sentence_transformers import SentenceTransformer

import os

"""Simple FAISS-based retriever for decision explanations.

Before using this module be sure an index has been built.  You can
create the index by running::

    python -m app.rag.index

The retriever will raise a clear RuntimeError if the files are missing.
"""

INDEX_PATH = "app/rag/faiss.index"
META_PATH = "app/rag/meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

# ensure index and metadata exist before trying to read them
if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
    # try to build automatically (requires DB access)
    try:
        from app.rag.index import build_faiss_index
        build_faiss_index()
    except Exception as e:
        raise RuntimeError(
            "FAISS index missing and auto-build failed: " + str(e)
        )
    # after building, check again
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        raise RuntimeError(
            f"FAISS index still not found after build; please run:\n"
            f"    python -m app.rag.index\n"
            f"Expected files: {INDEX_PATH}, {META_PATH}"
        )

index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)


def retrieve_insights(query: str, k: int = 5):
    q_emb = model.encode([query])
    distances, indices = index.search(q_emb, k)

    results = []
    for i in indices[0]:
        results.append(metadata[i])

    return results