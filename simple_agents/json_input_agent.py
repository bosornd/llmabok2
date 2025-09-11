from typing_extensions import override
from typing import AsyncGenerator
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.adk.events.event_actions import EventActions

class JsonInputAgent(BaseAgent):
    """
    Agent that parses JSON from user content and adds it to session state.
    """
    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        yield Event(author=self.name, invocation_id=ctx.invocation_id)

