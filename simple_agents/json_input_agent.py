import json
from typing_extensions import override
from typing import AsyncGenerator
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.adk.events.event_actions import EventActions

class JsonInputAgent(BaseAgent):
    """
    Agent that parses JSON from ctx.user_content.parts[0].text and adds it to session state.
    """
    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        try:
            text = ctx.user_content.parts[0].text
            yield Event(author=self.name, invocation_id=ctx.invocation_id, content=ctx.user_content,
                        actions=EventActions(state_delta=json.loads(text)))
        except Exception:
            yield Event(author=self.name, invocation_id=ctx.invocation_id, content=ctx.user_content,
                        error_message="Invalid JSON input provided.")
