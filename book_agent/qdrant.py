import os
import json

json_path = os.path.join(os.path.dirname(__file__), "best-seller-books.json")
with open(json_path, "r", encoding="utf-8") as f:
    books = json.load(f)

# pip install sentence-transformers hf_xet
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client.models import PointStruct
points = [PointStruct(id=idx+1, vector=model.encode(book["description"]).tolist(), payload=book)
          for idx, book in enumerate(books)]

from qdrant_client import QdrantClient
client = QdrantClient() # Connect to Qdrant (default: localhost:6333)

from qdrant_client.models import VectorParams, Distance
collection_name = "books"
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
)

client.upsert(collection_name=collection_name, points=points)

near_points = client.query_points(
    collection_name=collection_name,
    query=model.encode("역사와 인간의 본질을 다룬 충격적이고 도발적이라고 평가된 한강의 소설에 대해 알려줘").tolist(),
    limit=3
)

print(near_points)