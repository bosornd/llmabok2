import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent, Part

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=root_agent.name, user_id="user1")

    request = "회식 비용 $250을 환급해주세요."

asyncio.run(main())