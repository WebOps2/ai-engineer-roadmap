from .chroma_client import get_vector_store


def retrieve_document(query: str):
    db = get_vector_store()
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5},
    )
    return retriever.invoke(query)


if __name__ == "__main__":
    query = "Arsenal against Aston Villa in 2006-2007"
    documents = retrieve_document(query)

    for i, doc in enumerate(documents, start=1):
        print(f"\nRelevant Document {i}:")
        print(f"Content: {doc.page_content}")
        if doc.metadata:
            print(f"Metadata: {doc.metadata}")