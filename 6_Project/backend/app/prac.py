from chroma_client import get_vector_store

db = get_vector_store()

result = db.get(
    ids=["results.csv:0"],
    include=["embeddings"],
)
embedding = result["embeddings"]
print(embedding)