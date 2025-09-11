import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner

from google.genai.types import UserContent, Part

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)

    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    import os
    program_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(program_dir, "image.jpg")
    with open(image_path, "rb") as f:
        image_data = f.read()

    image = Part.from_bytes(data=image_data, mime_type="image/jpeg")
    await runner.artifact_service.save_artifact(app_name=session.app_name,
                                         user_id=session.user_id, session_id=session.id,
                                         filename="image.jpg", artifact=image)

    for event in runner.run(
        user_id=session.user_id, session_id=session.id,
        new_message=UserContent("image.jpg 파일에 대해 설명해줘.")
    ):
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}")

    session = await runner.session_service.get_session(app_name=session.app_name,
                                                       user_id=session.user_id,
                                                       session_id=session.id)
    print(session.events)

asyncio.run(main())