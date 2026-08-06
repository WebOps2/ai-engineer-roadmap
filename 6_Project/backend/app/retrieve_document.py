from .chroma_client import get_vector_store


# def retrieve_document(query: str):
#     db = get_vector_store()
#     retriever = db.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 3},
#     )
#     return retriever.invoke(query)

def retrieve_document(query: str):
    db = get_vector_store()

    results = db.similarity_search_with_relevance_scores(
        query,
        k=5,
    )

    return [
        document
        for document, score in results
        if score >= 0.2
    ]

if __name__ == "__main__":
    query = "team: Manchester City, wins, total_yel_card, total_red_card, season: 2013-2014"
    documents = retrieve_document(query)

    for i, doc in enumerate(documents, start=1):
        print(f"\nRelevant Document {i}:")
        print(f"Content: {doc.page_content}")
        if doc.metadata:
            print(f"Metadata: {doc.metadata}")