from typing_extensions import override
from typing import AsyncGenerator, Optional
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.adk.events.event_actions import EventActions

class WhileAgent(BaseAgent):
    """
    Custom agent to orchestrate a workflow with a condition.
    This agent runs a sequence of sub-agents while a specified condition is met.
    """
    condition: str
    max_iterations: Optional[int] = None

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        yield Event(author=self.name, invocation_id=ctx.invocation_id)

