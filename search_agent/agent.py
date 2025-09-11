from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 질문에 필요한 정보를 google_search 도구로 검색하고, 검색 결과를 근거로 답하세요.",
    tools=[google_search],
)
