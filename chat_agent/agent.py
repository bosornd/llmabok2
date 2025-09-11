from google.adk.agents import Agent

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
    instruction="너는 나의 친구야. 편안한 말투로 대화해줘.",
)