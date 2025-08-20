from google.adk.agents import Agent

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
#    description="Agent to engage in everyday conversations with users.",
    instruction="You are a friendly agent who can have casual, everyday conversations with users."
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import UserContent

    async def main():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=root_agent.name, user_id="user1")
        runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service)

        print("일상적인 대화를 지원하는 에이전트입니다. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit": break

#            async for event in runner.run_async(
            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
#                print(event)
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")

    asyncio.run(main())
