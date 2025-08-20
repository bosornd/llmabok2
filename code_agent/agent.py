from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    name="code_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    description="Executes Python code to perform calculations.",
    instruction="You are a calculator agent. Write and execute Python code to calculate the given expression. Return only the final numerical result as plain text, without markdown or code blocks.",
    include_contents='none'
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import UserContent

    async def main():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=root_agent.name, user_id="user1")
        runner = Runner(agent=root_agent, app_name=root_agent.name, session_service=session_service)

        print("파이썬 프로그램을 작성해서 문제를 해결합니다. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("해결할 문제: ")
            if user_input.lower() == "exit": break

            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
                print(event)

                if event.is_final_response():
                    for part in event.content.parts:
                        if part.executable_code:
                            print(f"Executing code:\n{part.executable_code.code}")
                        elif part.code_execution_result:
                            print(f"Code execution result: {part.code_execution_result.output}")
                        elif part.text:
                            print(f"Agent: {part.text}")

    asyncio.run(main())