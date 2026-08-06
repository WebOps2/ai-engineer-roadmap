from pathlib import Path

from langchain_community.document_loaders import CSVLoader

from .chroma_client import get_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_PATH = PROJECT_ROOT / "documents" / "results.csv"
BATCH_SIZE = 250


def load_documents():
    loader = CSVLoader(file_path=DOCUMENT_PATH)
    documents = loader.load()

    for document in documents:
        document.metadata["source"] = DOCUMENT_PATH.name

    return documents


def upload_documents(documents):
    vector_store = get_vector_store()

    if vector_store.get(include=[])["ids"]:
        print("The cloud collection already contains documents")
        return vector_store

    document_ids = [
        f"results.csv:{document.metadata['row']}" for document in documents
    ]

    for start in range(0, len(documents), BATCH_SIZE):
        end = start + BATCH_SIZE
        vector_store.add_documents(
            documents=documents[start:end],
            ids=document_ids[start:end],
        )
        print(f"Uploaded {min(end, len(documents))}/{len(documents)} documents")

    return vector_store


if __name__ == "__main__":
    documents = load_documents()
    upload_documents(documents)