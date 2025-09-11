from google.adk.agents import Agent

root_agent = Agent(
    name="country_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 {country}에 관한 질문에 답하세요.",
)