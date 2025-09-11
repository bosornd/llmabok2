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
)
