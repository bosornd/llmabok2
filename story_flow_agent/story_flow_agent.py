from typing import override
from typing import AsyncGenerator

import logging
logger = logging.getLogger(__name__)

from google.adk.agents import BaseAgent, Agent
from google.adk.agents import InvocationContext
from google.adk.events import Event

from .sub_agents import COMPLETION_PHRASE

class StoryFlowAgent(BaseAgent):
    """
    Custom agent for a story generation and refinement workflow.

    This agent orchestrates a sequence of LLM agents to generate a story,
    critique it, revise it, check grammar and tone, and potentially
    regenerate the story if the tone is negative.
    """

    # --- Field Declarations for Pydantic ---
    # Declare the agents passed during initialization as class attributes with type hints
    story_generator: Agent
    critic: Agent
    reviser: Agent
    tone_check: Agent

    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        story_generator: Agent,
        critic: Agent,
        reviser: Agent,
        tone_check: Agent,
    ):
        """
        Initializes the StoryFlowAgent.

        Args:
            name: The name of the agent.
            story_generator: An Agent to generate the initial story.
            critic: An Agent to critique the story.
            reviser: An Agent to revise the story based on criticism.
            tone_check: An Agent to analyze the tone.
        """

        # Pydantic will validate and assign them based on the class annotations.
        super().__init__(
            name=name,
            story_generator=story_generator,
            critic=critic,
            reviser=reviser,
            tone_check=tone_check,
            sub_agents=[story_generator, critic, reviser, tone_check],
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        Implements the custom orchestration logic for the story workflow.
        Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
        """
        logger.info(f"[{self.name}] Starting story generation workflow.")

        for i in range(3):  # Retry up to 3 times if tone is negative
            logger.info(f"[{self.name}] Iteration {i+1} of generation loop...")

            # 1. Initial Story Generation
            logger.info(f"[{self.name}] Running StoryGenerator...")
            async for event in self.story_generator.run_async(ctx):
                logger.info(f"[{self.name}] Event from StoryGenerator: {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event

            # Check if story was generated before proceeding
            if "story" not in ctx.session.state or not ctx.session.state["story"]:
                logger.error(f"[{self.name}] Failed to generate initial story. Aborting workflow.")
                return # Stop processing if initial story failed

            logger.info(f"[{self.name}] Story state after generator: {ctx.session.state.get('story')}")

            # 2. Critic-Reviser Loop
            for j in range(3):
                logger.info(f"[{self.name}] Iteration {j+1} of refinement loop...")

                # Critic
                logger.info(f"[{self.name}] Running Critic...")
                async for event in self.critic.run_async(ctx):
                    logger.info(f"[{self.name}] Event from Critic: {event.model_dump_json(indent=2, exclude_none=True)}")
                    yield event

                # Check if story was revised before proceeding
                if "criticism" not in ctx.session.state or not ctx.session.state["criticism"]:
                    logger.error(f"[{self.name}] Failed to criticize story. Aborting workflow.")
                    return

                if ctx.session.state["criticism"].strip() == COMPLETION_PHRASE:
                    break       # Exit loop if no more revision is needed

                # Reviser
                logger.info(f"[{self.name}] Running Revisor...")
                async for event in self.reviser.run_async(ctx):
                    logger.info(f"[{self.name}] Event from Revisor: {event.model_dump_json(indent=2, exclude_none=True)}")
                    yield event

            logger.info(f"[{self.name}] Story state after loop: {ctx.session.state.get('story')}")

            # 3. Sequential Post-Processing (Tone Check)
            logger.info(f"[{self.name}] Running ToneCheck...")
            async for event in self.tone_check.run_async(ctx):
                logger.info(f"[{self.name}] Event from ToneCheck: {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event

            # 4. Tone-Based Conditional Logic
            tone_check_result = ctx.session.state.get("tone_check_result")
            logger.info(f"[{self.name}] Tone check result: {tone_check_result}")

            if tone_check_result.strip() == "negative":
                logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
            else:
                logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
                break
        
        logger.info(f"[{self.name}] Workflow finished.")