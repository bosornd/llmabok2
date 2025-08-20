# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        You are an agent whose job is to handle the reimbursement process for
        the employees. If the amount is less than $100, you will automatically
        approve the reimbursement.

        If the amount is greater than $100, you will
        ask for approval from the manager. If the manager approves, you will
        call reimburse() to reimburse the amount to the employee. If the manager
        rejects, you will inform the employee of the rejection.
    """,
    tools=[reimburse, LongRunningFunctionTool(func=ask_for_approval)]
)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import asyncio
    from typing import Any
    from google.adk.events import Event
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    APP_NAME = "human_in_the_loop"
    USER_ID = "1234"
    SESSION_ID = "session1234"

    # Session and Runner
    async def setup_session_and_runner():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
        return session, runner


    # Agent Interaction
    async def call_agent_async(query):

        def get_long_running_function_call(event: Event) -> types.FunctionCall:
            # Get the long running function call from the event
            if not event.long_running_tool_ids or not event.content or not event.content.parts:
                return
            for part in event.content.parts:
                if (
                    part
                    and part.function_call
                    and event.long_running_tool_ids
                    and part.function_call.id in event.long_running_tool_ids
                ):
                    return part.function_call

        def get_function_response(event: Event, function_call_id: str) -> types.FunctionResponse:
            # Get the function response for the fuction call with specified id.
            if not event.content or not event.content.parts:
                return
            for part in event.content.parts:
                if (
                    part
                    and part.function_response
                    and part.function_response.id == function_call_id
                ):
                    return part.function_response

        content = types.Content(role='user', parts=[types.Part(text=query)])
        session, runner = await setup_session_and_runner()

        print("\nRunning agent...")
        events = runner.run_async(session_id=session.id, user_id=USER_ID, new_message=content)

        long_running_function_call, long_running_function_response, ticket_id = None, None, None
        async for event in events:
            # Use helper to check for the specific auth request event
            if not long_running_function_call:
                long_running_function_call = get_long_running_function_call(event)
            elif not long_running_function_response:
                long_running_function_response = get_function_response(event, long_running_function_call.id)

            if event.content and event.content.parts:
                if text := ''.join(part.text or '' for part in event.content.parts):
                    print(f'[{event.author}]: {text}')

        if long_running_function_response:
            # send back an intermediate / final response
            updated_response = long_running_function_response.model_copy(deep=True)
            updated_response.response = {'status': 'approved'}

            async for event in runner.run_async(
            session_id=session.id, user_id=USER_ID, new_message=types.Content(parts=[types.Part(function_response = updated_response)], role='user')
            ):
                if event.content and event.content.parts:
                    if text := ''.join(part.text or '' for part in event.content.parts):
                        print(f'[{event.author}]: {text}')


    # reimbursement that doesn't require approval
    asyncio.run(call_agent_async("Please reimburse 50$ for meals"))

    # reimbursement that requires approval
    asyncio.run(call_agent_async("Please reimburse 200$ for meals"))
