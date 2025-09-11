from google.adk.agents import Agent
from google.adk.tools import AgentTool

summarizer = Agent(
    name="summarizer",
    model="gemini-2.0-flash",
    description="Agent to summarize text",
    instruction="주어진 내용을 간결하게 요약하십시오.",
)

root_agent = Agent(
    name="summary_agent",
    model="gemini-2.0-flash",
    instruction="""당신은 유용한 도우미입니다.
        사용자가 텍스트 요약을 요청하면 'summarizer'에게 요청하세요.""",
    sub_agents=[summarizer],
)

root_agent = Agent(
    name="summary_agent",
    model="gemini-2.0-flash",
    instruction="""당신은 유용한 도우미입니다.
        사용자가 텍스트 요약을 요청하면 'summarizer' 도구를 사용하세요.""",
    tools=[AgentTool(agent=summarizer)],
)
