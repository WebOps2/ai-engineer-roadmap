from pathlib import Path

from langchain_community.document_loaders import CSVLoader

from .chroma_client import get_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_PATH = PROJECT_ROOT / "documents" / "results.csv"
BATCH_SIZE = 250


def load_documents(doc_path: Path):
    loader = CSVLoader(file_path=doc_path)
    documents = loader.load()

    for document in documents:
        document.metadata["source"] = doc_path.name

    return documents


def upload_documents(documents):
    vector_store = get_vector_store()

    # if vector_store.get(include=[])["ids"]:
    #     print("The cloud collection already contains documents")
    #     return vector_store

    document_ids = [
        f"{document.metadata['source']}:{document.metadata['row']}"
        for document in documents
    ]
    
    existing = vector_store.get(
        ids=document_ids,
        include=[],
    )
    existing_ids = set(existing["ids"])
    new_documents = []
    new_ids = []
    for document, document_id in zip(documents, document_ids):
        if document_id not in existing_ids:
            new_documents.append(document)
            new_ids.append(document_id)

    for start in range(0, len(documents), BATCH_SIZE):
        end = start + BATCH_SIZE
        vector_store.add_documents(
            documents=new_documents[start:end],
            ids=new_ids[start:end],
        )
        print(f"Uploaded {min(end, len(documents))}/{len(documents)} documents")

    return vector_store


if __name__ == "__main__":
    stats_path = PROJECT_ROOT / "documents" / "stats.csv"
    documents = load_documents(stats_path)
    upload_documents(documents)