from google.adk.agents import Agent

def add(a: float, b: float) -> float:
    """Adds two floats and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The sum of the two floats.
    """
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second float from the first and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The difference of the two floats.
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two floats and returns the result.

    Args:
        a (float): The first float.
        b (float): The second float.

    Returns:
        float: The product of the two floats.
    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divides the first float by the second and returns the result.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The quotient of the two floats.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

root_agent = Agent(
    name="math_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about mathematical operations."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about mathematical operations."
    ),
    tools=[add, subtract, multiply, divide],
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

        print("간단한 계산을 지원하는 에이전트입니다. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit": break

#            async for event in runner.run_async(
            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
#                print(event)
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")

            """
            events = list(runner.run(user_id=session.user_id,
                                    session_id=session.id,
                                    new_message=UserContent(user_input)))
            print(f"Agent: {events[-1].content.parts[0].text}")
            """

    asyncio.run(main())

