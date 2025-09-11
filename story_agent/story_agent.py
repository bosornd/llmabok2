from typing_extensions import override
from typing import AsyncGenerator, Optional
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event

class StoryAgent(BaseAgent):
    """
    Custom agent to orchestrate a story generation workflow.
    This agent runs a sequence of sub-agents to generate, critique, and refine a story.
    The process stops if the critic agent returns "No major issues found."
    """
    generator: BaseAgent
    critic: BaseAgent
    reviser: BaseAgent

    max_iterations: Optional[int] = None

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        async for event in self.generator.run_async(ctx):
            yield event

