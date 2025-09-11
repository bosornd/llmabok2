# pip install qdrant-client
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")

from qdrant_client.models import Distance, VectorParams
client.recreate_collection(
    collection_name="star",
    vectors_config=VectorParams(size=2, distance=Distance.EUCLID),
                                        # Distance.COSINE, Distance.DOT
)

from qdrant_client.models import PointStruct
points=[
    PointStruct(id=0, vector=[1, 1], payload={"planet": "Mercury"}),
    PointStruct(id=1, vector=[-1, 2], payload={"planet": "Venus"}),
    PointStruct(id=2, vector=[3, 1], payload={"planet": "Earth"}),
    PointStruct(id=3, vector=[-2, -3], payload={"planet": "Mars"}),
    PointStruct(id=4, vector=[4, -4], payload={"planet": "Jupiter"}),
    PointStruct(id=5, vector=[6, 4], payload={"planet": "Saturn"}),
]

client.upsert(collection_name="star", points=points)

near_points = client.query_points(
    collection_name="star",
    query=[2, 1],
    limit=3
)

print(near_points)

# using Distance.EUCLID
# points=[ScoredPoint(id=2, version=0, score=1.0, payload={'planet': 'Earth'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=0, version=0, score=1.0, payload={'planet': 'Mercury'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=1, version=0, score=3.1622777, payload={'planet': 'Venus'}, vector=None, shard_key=None, order_value=None)]

# using Distance.COSINE
# points=[ScoredPoint(id=5, version=0, score=0.99227786, payload={'planet': 'Saturn'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=2, version=0, score=0.98994946, payload={'planet': 'Earth'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=0, version=0, score=0.94868326, payload={'planet': 'Mercury'}, vector=None, shard_key=None, order_value=None)]

# using Distance.DOT
# points=[ScoredPoint(id=5, version=0, score=16.0, payload={'planet': 'Saturn'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=2, version=0, score=7.0, payload={'planet': 'Earth'}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=4, version=0, score=4.0, payload={'planet': 'Jupiter'}, vector=None, shard_key=None, order_value=None)]
