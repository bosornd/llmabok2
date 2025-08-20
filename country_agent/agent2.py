from pydantic import BaseModel, Field

class CountryInput(BaseModel):
    country: str = Field(description="The country to get information about.")

class CapitalInfoOutput(BaseModel):
    country: str = Field(description="The country to get information about.")
    capital: str = Field(description="The capital city of the country.")

import json
from google.adk.agents import Agent
root_agent = Agent(
    name="country_agent",
    model="gemini-2.0-flash",
#    description="Agent to provide capital in a specific JSON format.",
#    instruction="""You are an agent that provides country information.
#The user will provide the country name in a JSON format like {{"country": "country_name"}}.
#Respond ONLY with a JSON object matching this exact schema:
#{json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
#""",
    description="국가의 수도 정보를 제공하는 에이전트입니다.",
    instruction=f"""사용자는 {{"country": "한국"}}와 같은 JSON 형식으로 국가 이름을 제공합니다.
정확히 다음 스키마에 맞는 JSON 객체로만 응답하십시오:
{json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
""",
    input_schema=CountryInput,
    output_schema=CapitalInfoOutput,
    output_key="output",
    include_contents='none',  # 이전 대화의 내용은 포함하지 않음
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio
    import json

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import UserContent

    async def main():
        session_service = InMemorySessionService()
        runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service)
        session = await session_service.create_session(app_name=root_agent.name, user_id="user1")

        print("국가의 수도 정보를 제공하는 에이전트입니다. 궁금한 국가를 입력하세요. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("Country: ")
            if user_input.lower() == "exit": break

            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(f"{{\"country\": \"{user_input}\"}}")
            ):
                print(event)
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")

            print(session.state)        # {}

            session = await session_service.get_session(app_name=root_agent.name,
                                                  user_id=session.user_id,
                                                  session_id=session.id)

            print(session.state)        # {'output': {'capital': '서울'}}

            result = session.state.get(root_agent.output_key, None)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    asyncio.run(main())