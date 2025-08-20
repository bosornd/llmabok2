from .story_flow_agent import StoryFlowAgent
from .sub_agents import story_generator, critic, reviser, tone_check

root_agent = StoryFlowAgent(
    name="story_flow_agent",

    story_generator=story_generator,
    critic=critic,
    reviser=reviser,
    tone_check=tone_check,
)
