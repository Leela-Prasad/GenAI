from langchain.embeddings.base import Embeddings
from typing import List
import requests

class CustomEmbeddings(Embeddings):
    endpoint: str
    model: str
    
    def __init__(self, endpoint: str, model: str):
        self.endpoint = endpoint
        self.model = model
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        
        for text in texts:
            response = requests.post(
                url=f"{self.endpoint}/v1/embeddings",
                headers={"Content-Type": "application/json"},
                json={
                    "input": text,
                    "model": self.model
                }
            )
            response.raise_for_status()
            data = response.json()
            embeddings.append(data["data"][0]["embedding"])

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        response = requests.post(
            url=f"{self.endpoint}/v1/embeddings",
            headers={
                # Authorization
                "Content-Type": "application/json"
            },
            json={
                "input": text,
                "model": self.model
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return data["data"][0]["embedding"]
    
    

from langchain_community.vectorstores import FAISS

embedding_model = CustomEmbeddings(
    endpoint="http://localhost:8000",
    model="text-embedding-3-small"
)

texts = [
    "LangChain makes LLM orchestration easy",
    "FAISS is a fast vector database",
    "FastAPI is great for building AI services"
]

vectorstore = FAISS.from_texts(
    texts=texts,
    embedding=embedding_model
)


results = vectorstore.similarity_search(
    "How do I store embeddings?",
    k=2
)
print(results)