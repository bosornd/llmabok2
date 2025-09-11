from typing_extensions import override
from typing import Callable, Any, AsyncGenerator, List, Optional
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.adk.events.event_actions import EventActions
from google.genai.types import ModelContent

class LambdaAgent(BaseAgent):
    """
    Agent that wraps a user-provided function and executes it as part of the agent workflow.
    Allows specifying input keys and output key for session state.
    """
    func: Callable[..., Any]
    input_keys: List[str]
    output_key: Optional[str] = None

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        yield Event(author=self.name, invocation_id=ctx.invocation_id)
