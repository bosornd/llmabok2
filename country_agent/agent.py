from google.adk.agents import Agent

root_agent = Agent(
    name="country_agent",
    model="gemini-2.0-flash",
    description=(
        "국가에 대한 정보를 제공하는 에이전트입니다."
#        "Agent to provide information about the given country."
#        "Agent to provide information about {country}."     # description에는 {country}가 해석되지 않는다.
    ),
    instruction=(
        "사용자의 {country}에 관한 질문에 답하세요."     # 한글로 작성된 instruction은 잘 동작하지 않는다.
#        "You are a helpful agent who can answer user questions about {country}."
    ),
)
"""
# 다음과 같이 system_instruction으로 LLM에게 지시된다.
system_instruction: "사용자의 중국에 관한 질문에 답하세요. You are an agent. Your internal name is "country_agent". The description about you is "Agent to provide information about the given country.""
"""


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import UserContent

    async def main():
        session_service = InMemorySessionService()
        runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service)

        print("국가에 대한 정보를 제공하는 에이전트입니다. 궁금한 국가를 입력하세요. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("Country: ")
            if user_input.lower() == "exit": break

            session = await session_service.create_session(app_name=root_agent.name, user_id="user1",
                                                           state={"country": user_input})
            
            print(f"{user_input}에 대해 궁금한 것을 질문하세요. 'exit' 입력 시 종료됩니다.")
            while True:
                user_input = input("User: ")
                if user_input.lower() == "exit": break

                for event in runner.run(
                    user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
                ):
                    print(event)
                    if event.is_final_response():
                        print(f"Agent: {event.content.parts[0].text}")

    asyncio.run(main())