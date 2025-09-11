from google.adk.agents import Agent
from google.adk.tools import exit_loop

GEMINI_MODEL = "gemini-2.0-flash"

initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=GEMINI_MODEL,
    output_key="story",
)

critic_agent = Agent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    output_key="criticism",
)

refiner_agent = Agent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    output_key="story",
    tools=[exit_loop],
)
