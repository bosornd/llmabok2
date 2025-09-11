import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent, Part

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    request = "회식 비용 $250을 환급해주세요."

    approval_request = None
    for event in runner.run(user_id=session.user_id, session_id=session.id,
                            new_message=UserContent(request)):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_response:
                    if part.function_response.name == "ask_for_approval":
                        approval_request = part.function_response
                elif part.text:
                    print(f"Agent: {part.text}")

    if approval_request:
        result = input("Enter your response(approve or reject): ")
        approval_response = approval_request.model_copy(deep=True)
        approval_response.response["status"] = "approved" if result == "approve" else "rejected"

        for event in runner.run(user_id=session.user_id, session_id=session.id,
                                new_message=UserContent(parts=[Part(function_response=approval_response)])):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

    session = await runner.session_service.get_session(app_name=session.app_name, user_id=session.user_id, session_id=session.id)
    print(session.events)


asyncio.run(main())