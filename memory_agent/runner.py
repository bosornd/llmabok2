import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)

    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")


    print("일상적인 대화를 나누는 에이전트입니다.")
    print("'new' 입력 시 새로운 대화가 시작됩니다. 'exit' 입력 시 종료됩니다.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit": break
        elif user_input.lower() == "new":
            session = await runner.session_service.get_session(app_name=session.app_name, user_id=session.user_id, session_id=session.id)
            await runner.memory_service.add_session_to_memory(session)

            # 신규 대화 세션 생성
            session = await runner.session_service.create_session(app_name=session.app_name, user_id=session.user_id)
        else:
            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")


asyncio.run(main())