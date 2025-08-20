from google.adk.agents import Agent
from google.adk.tools import AgentTool

summary_agent = Agent(
    model="gemini-2.0-flash",
    name="summary_agent",
    instruction="""주어진 내용을 간결하게 요약하십시오.""",
    description="Agent to summarize text",
)

root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    instruction="""당신은 유용한 도우미입니다.
        사용자가 텍스트 요약을 요청하면 'summary_agent'에게 요청하세요.""",
    sub_agents=[summary_agent],
)

root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    instruction="""당신은 유용한 도우미입니다.
        사용자가 제공한 텍스트를 요약하기 위해 'summarize' 도구를 사용하십시오.
        사용자의 메시지를 수정하거나 요약하지 않고 'summarize' 도구에 정확히 전달하십시오.
        도구의 응답을 사용자에게 제시하십시오.""",
    tools=[AgentTool(agent=summary_agent)]
)
