from typing import Any

def ask_for_approval(purpose: str, amount: float) -> dict[str, Any]:
    """Ask for approval for the reimbursement."""
    return {'status': 'pending', 'purpose' : purpose, 'amount': amount, 'ticket-id': 'approval-ticket-1'}

def reimburse(purpose: str, amount: float) -> dict[str, Any]:
    """Reimburse the amount of money to the employee."""
    return {'status': 'approved', 'purpose' : purpose, 'amount': amount}

from google.adk.agents import Agent
from google.adk.tools import LongRunningFunctionTool

root_agent = Agent(
    model="gemini-2.0-flash",
    name="reimbursement_agent",
    instruction="""
        당신은 직원의 환급 프로세스를 처리하는 에이전트입니다.
        $100 이하의 요청은 자동으로 승인합니다. 'reimburse'를 호출합니다.
        $100 초과의 요청은 관리자의 승인을 요청합니다. 'ask_for_approval'을 호출합니다.
        관리자가 승인하면 'reimburse'를 호출하여 환급을 처리합니다.
        관리자가 거부하면 직원에게 거부 사실을 알립니다.
    """,
    tools=[reimburse, LongRunningFunctionTool(func=ask_for_approval)]
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio

    from google.adk.runners import InMemoryRunner
    from google.genai.types import UserContent, Part

    async def main():
        runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
        session = await runner.session_service.create_session(app_name=root_agent.name, user_id="user1")

        request = "회식 비용 $200을 환급해주세요."
        for event in runner.run(user_id=session.user_id, session_id=session.id,
                                new_message=UserContent(request)):
            if event.content and event.content.parts:
                part = event.content.parts[0]

                if part.function_response:
                    print(f"Function response: {part.function_response.response}")
                    approval_request = part.function_response
                elif part.text:
                    print(f"Agent: {part.text}")

        result = input("Enter your response(approve or reject): ")
        approval_response = approval_request.model_copy(deep=True)
        approval_response.response["status"] = "approved" if result == "approve" else "rejected"

        for event in runner.run(user_id=session.user_id, session_id=session.id,
                                new_message=UserContent(parts=[Part(function_response=approval_response)])):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

    asyncio.run(main())
