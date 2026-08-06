from functools import lru_cache
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
COLLECTION_NAME = "premier_league_results"

load_dotenv(REPOSITORY_ROOT / ".env", override=True)


def require_environment_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    client = chromadb.CloudClient(
        api_key=require_environment_variable("CHROMA_API_KEY"),
        tenant=require_environment_variable("CHROMA_TENANT"),
        database=require_environment_variable("CHROMA_DATABASE"),
        cloud_host=require_environment_variable("CHROMA_HOST"),
    )
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    return Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )


if __name__ == "__main__":
    get_vector_store()
    print("Connected to Chroma Cloud")
    print(f"Collection: {COLLECTION_NAME}")
