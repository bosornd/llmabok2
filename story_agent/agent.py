from google.adk.agents import SequentialAgent, LoopAgent
from .sub_agents import initial_writer_agent, critic_agent, refiner_agent

root_agent = SequentialAgent(
    name="WritingPipeline",
    sub_agents=[
        initial_writer_agent,
        LoopAgent(
            name="RefinementLoop",
            sub_agents=[critic_agent, refiner_agent],
            max_iterations=5 # Limit loops
        )
    ],
)

from .sub_agents import story_agent
root_agent = story_agent