import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.core.database import SessionLocal

INDEX_PATH = "app/rag/faiss.index"
META_PATH = "app/rag/meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_faiss_index():
    session = SessionLocal()

    query = text("""
        SELECT
            d.customer_id,
            ca.action_type,
            d.explanation
        FROM decisions d
        JOIN candidate_actions ca
          ON d.chosen_action = ca.action_id
        LIMIT 5000
    """)

    rows = session.execute(query).fetchall()
    session.close()

    documents = []
    metadata = []

    for r in rows:
        text_doc = (
            f"Customer {r.customer_id} decision {r.action_type}. "
            f"Explanation: {r.explanation}"
        )
        documents.append(text_doc)
        metadata.append({
            "customer_id": r.customer_id,
            "action": r.action_type
        })

    embeddings = model.encode(documents, show_progress_bar=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # make sure output directory exists
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("FAISS index built.")


if __name__ == "__main__":
    build_faiss_index()