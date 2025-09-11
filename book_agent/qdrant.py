import json
with open("best-seller-books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# pip install sentence-transformers hf_xet
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client.models import PointStruct
points = [PointStruct(id=idx+1, vector=model.encode(book["description"]).tolist(),
                      payload=book) for idx, book in enumerate(books)]

