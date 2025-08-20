from typing_extensions import override
from typing import AsyncGenerator, Optional

from google.adk.agents import BaseAgent
from google.adk.agents import InvocationContext
from google.adk.events import Event

class WhileAgent(BaseAgent):
    """
    Custom agent to orchestrate a workflow with a condition.
    This agent runs a sequence of sub-agents while a specified condition is met.
    """
    # --- Field Declarations for Pydantic ---
    # Declare the agents passed during initialization as class attributes with type hints
    condition: str
    max_iterations: Optional[int] = None

    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    model_config = {"arbitrary_types_allowed": True}

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        Implements the custom orchestration logic for the workflow.
        This method runs the sub-agents in sequence while the condition is met.
        """
        running = True
        times_looped = 0
        while running and (not self.max_iterations or times_looped < self.max_iterations):
            times_looped += 1
            for agent in self.sub_agents:
                try:
                    running = eval(self.condition, {}, ctx.session.state)
                except Exception as e:
                    pass
                
                if not running: break
            
                async for event in agent.run_async(ctx):
                    yield event

# {"number" : 1} -> increase_agent -> {"number" : 2}