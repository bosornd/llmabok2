from google.adk.agents import Agent
from google.adk. tools import load_artifacts

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 질문에 답하세요. 사용자가 요청한 파일을 불러오려면 'load_artifacts' 도구를 사용하세요.",
    tools=[load_artifacts]
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import Runner, InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    from google.adk.artifacts import InMemoryArtifactService
    from google.genai.types import UserContent, Part

    async def main():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=root_agent.name, user_id="user1")
        artifact_service = InMemoryArtifactService()
        runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service, artifact_service=artifact_service)

        with open("그림.jpg", "rb") as f:
            image_data = f.read()
        image = Part.from_bytes(data=image_data, mime_type="image/jpeg")
        await artifact_service.save_artifact(app_name=session.app_name, user_id=session.user_id, session_id=session.id, filename="image.jpg", artifact=image)

        for event in runner.run(
            user_id=session.user_id, session_id=session.id, new_message=UserContent("image.jpg 파일에 대해 설명해줘.")
        ):
            print(event)
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

    asyncio.run(main())