from google.adk.agents import Agent

from datetime import datetime
def get_today() -> str:
    """
    오늘의 날짜와 요일을 반환합니다.
    """
    return datetime.now().strftime("%Y-%m-%d %A")

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
    instruction=f"사용자의 날짜와 요일에 관한 질문에 답하세요. 오늘 날짜와 요일은 {get_today()}입니다.",
)

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
    instruction=(
        "사용자의 날짜와 요일에 관한 질문에 답하세요. 오늘 날짜와 요일은 'get_today' 도구를 사용해서 확인할 수 있습니다."
    ),
    tools=[get_today]
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

        print("날짜와 요일에 대해 답변하는 에이전트입니다. 'exit' 입력 시 종료됩니다.")
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
