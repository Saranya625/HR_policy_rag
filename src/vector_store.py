import os
from langchain_community.vectorstores import FAISS
import time
from src import config 
from src.embeddings import get_embeddings_model


# build_vector_store 

def build_vector_store(chunks):
    """Build FAISS vector store with controlled Jina embedding batches."""

    if not chunks:
        raise ValueError("No chunks provided.")

    print("=" * 60)
    print("Inside build_vector_store")
    print("Chunks:", len(chunks))

    embeddings_model = get_embeddings_model()

    batch_size = 25
    vector_store = None

    for start in range(0, len(chunks), batch_size):

        batch = chunks[start:start + batch_size]

        print(
            f"Embedding chunks "
            f"{start + 1}-{min(start + batch_size, len(chunks))} "
            f"of {len(chunks)}"
        )

        if vector_store is None:
            vector_store = FAISS.from_documents(
                batch,
                embeddings_model
            )
        else:
            vector_store.add_documents(batch)

        # Give Jina's rate limit some breathing room
        time.sleep(2)

    print("FAISS vector store created successfully.")
    print("=" * 60)

    return vector_store

## save vector store 

def save_vector_store(vector_store, path: str = config.VECTOR_STORE_PATH) -> None:
    """Save the FAISS index to disk 
    so we don't have to rebuild it every time."""
    vector_store.save_local(path)


def load_vector_store(path: str = config.VECTOR_STORE_PATH):
    """Load a previously saved FAISS index from disk."""
    embeddings_model = get_embeddings_model()
    # allow_dangerous_deserialization is safe here because we only ever load
    # an index that this same app created and saved.
    return FAISS.load_local(path, embeddings_model, allow_dangerous_deserialization=True)


def vector_store_exists(path: str = config.VECTOR_STORE_PATH) -> bool:
    """Check if a saved FAISS index already exists on disk."""
    return os.path.exists(os.path.join(path, "index.faiss"))


def get_retriever(vector_store, k: int = config.TOP_K_RESULTS):
    """Turn a vector store into a retriever 
    that returns the top-k matching chunks."""
    return vector_store.as_retriever(search_kwargs={"k": k})