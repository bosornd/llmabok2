from google.adk.agents import Agent
from google.adk.tools import load_memory

root_agent = Agent(
    name="MemoryRecallAgent",
    model="gemini-2.0-flash",
    instruction="사용자와 일상적인 대화를 나누는 에이전트입니다. 질문에 답하기 위해서 이전 대화 내용이 필요하면 'load_memory' 도구를 사용합니다.",
    tools=[load_memory]
)

# InMemorySessionService.search_memory()는 영어 단어만 비교하면서 검색한다.
# 다국어 지원이 안됨.
