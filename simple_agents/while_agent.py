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
        running = True
        times_looped = 0
        while running and (not self.max_iterations or times_looped < self.max_iterations):
            times_looped += 1
            for agent in self.sub_agents:
                if running: running = eval(self.condition, {}, ctx.session.state)
                if not running: break
            
                async for event in agent.run_async(ctx):
                    yield event
                    if event.actions.escalate: running = False

