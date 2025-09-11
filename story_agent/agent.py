from google.adk.agents import SequentialAgent, LoopAgent
from .sub_agents import initial_writer_agent, critic_agent, refiner_agent

root_agent = initial_writer_agent
