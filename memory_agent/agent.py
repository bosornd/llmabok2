from google.adk.agents import Agent
from google.adk.tools import load_memory

root_agent = Agent(
    name="MemoryRecallAgent",
    model="gemini-2.0-flash",
    instruction="사용자와 일상적인 대화를 나누는 에이전트입니다. 질문에 답하기 위해서 이전 대화 내용이 필요하면 'load_memory' 도구를 사용합니다.",
    tools=[load_memory]
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.memory import InMemoryMemoryService
    from google.genai.types import UserContent

    async def main():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=root_agent.name, user_id="user1")

        memory_service = InMemoryMemoryService()
        runner = Runner(agent=root_agent, app_name=root_agent.name,
                        session_service=session_service, memory_service=memory_service)

        print("일상적인 대화를 나누는 에이전트입니다.")
        print("'new' 입력 시 새로운 대화가 시작됩니다. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit": break
            elif user_input.lower() == "new":
                # 이전 대화 내용을 메모리에 추가
                session = await session_service.get_session(app_name=root_agent.name, user_id="user1", session_id=session.id)
                await memory_service.add_session_to_memory(session)

                # 신규 대화 세션 생성
                session = await session_service.create_session(app_name=root_agent.name, user_id="user1")
            else:
                for event in runner.run(
                    user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
                ):
                    print(event)
                    if event.is_final_response():
                        print(f"Agent: {event.content.parts[0].text}")

    asyncio.run(main())

# InMemorySessionService.search_memory()는 영어 단어만 비교하면서 검색한다.
# 다국어 지원이 안됨.
