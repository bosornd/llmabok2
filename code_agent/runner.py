import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)

    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    print("파이썬 프로그램을 작성해서 문제를 해결합니다. 'exit' 입력 시 종료됩니다.")
    while True:
        user_input = input("해결할 문제: ")
        if user_input.lower() == "exit": break

        for event in runner.run(
            user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.executable_code:
                        print(f"Executing code:\n{part.executable_code.code}")
                    elif part.code_execution_result:
                        print(f"Code execution result: {part.code_execution_result.output}")
                    elif part.text:
                        print(f"Agent: {part.text}")

asyncio.run(main())