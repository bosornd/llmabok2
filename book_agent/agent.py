from google.adk.agents import Agent

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client import QdrantClient
client = QdrantClient()

root_agent = Agent(
    name="book_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 베스트셀러에 관한 질문에 답하세요.",
)
