from google.adk.agents import Agent
from google.adk.tools import load_artifacts

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 질문에 답하세요. 사용자가 요청한 파일을 불러오려면 'load_artifacts' 도구를 사용하세요.",
    tools=[load_artifacts]
)
