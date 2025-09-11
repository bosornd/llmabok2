from google.adk.agents import Agent

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client import QdrantClient
client = QdrantClient()

from qdrant_client.models import Filter, FieldCondition, MatchValue, Range, MatchText
def _parse_filter(filters: dict):
    """
    filter dict를 Qdrant Filter must 조건 리스트로 변환.
    지원 operator: eq, ne, gt, lt, gte, lte

    Args:
        filter (dict): 필터 조건 (예: {"author": "한강"})

    Returns:
        Filter: Qdrant의 Filter 객체
    """
    must_conditions = []
    should_conditions = []
    must_not_conditions = []

    for key, cond in filters.items():
        # 단순 eq: {"author": "한강"}
        if not isinstance(cond, dict):
            must_conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(value=cond)
                )
            )
            continue

        # operator 방식: {"author": {"ne": "한강"}}
        for op, value in cond.items():
            if op == "eq":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            elif op == "ne":
                must_not_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            elif op == "gt":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(gt=value)
                    )
                )
            elif op == "lt":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(lt=value)
                    )
                )
            elif op == "gte":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(gte=value)
                    )
                )
            elif op == "lte":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(lte=value)
                    )
                )
            # 텍스트 검색 지원 (예시)
            elif op == "text":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchText(text=value)
                    )
                )
            # 기타 연산자 필요시 추가

    return Filter(
        must=must_conditions if must_conditions else None,
        must_not=must_not_conditions if must_not_conditions else None,
        should=should_conditions if should_conditions else None
    )

def get_best_sellers(query: str, filter: dict, top_k: int = 3):
    """
    주어진 쿼리에 대해 벡터 유사도 검색을 통해 베스트셀러를 찾아서 반환합니다.

    Args:
        query (str): 검색할 쿼리 문자열
        filter (dict): 필터 조건 딕셔너리. 사용 가능한 key는 author, title, category, price, date가 있으며, 필터 조건은 key : value 또는 key : {operator : value}로 주어집니다. operator에는 "eq", "ne", "gt", "lt", "gte", "lte"가 있습니다. 예: [{"author": "한강"}, {"year": {"gte": 2020}}]
        top_k (int): 반환할 상위 k개의 책 수 (기본값: 3)

    Returns:
        List[dict]: 베스트셀러 리스트, 각 책은 딕셔너리 형태로 반환됩니다.
    """
    near_points = client.query_points(
        collection_name="books",
        query=model.encode(query).tolist(),
        query_filter=_parse_filter(filter),
        limit=top_k
    )

    return [point.payload for point in near_points.points]

root_agent = Agent(
    name="book_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 베스트셀러에 관한 질문에 답하세요.",
    tools=[get_best_sellers]
)
