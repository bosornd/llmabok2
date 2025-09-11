import json
import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)

    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    print("국가의 수도 정보를 제공하는 에이전트입니다. 궁금한 국가를 입력하세요. 'exit' 입력 시 종료됩니다.")
    while True:
        user_input = input("Country: ")
        if user_input.lower() == "exit": break

        for event in runner.run(
            user_id=session.user_id, session_id=session.id, new_message=UserContent(f"{{\"country\": \"{user_input}\"}}")
        ):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

        session = await runner.session_service.get_session(app_name=session.app_name,
                                                           user_id=session.user_id,
                                                           session_id=session.id)
        print(session.state)

        result = session.state.get(root_agent.output_key, None)
        print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(main())