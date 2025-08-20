from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.0-flash"
COMPLETION_PHRASE = "No major issues found."

story_generator = Agent(
    name="StoryGenerator",
    model=GEMINI_MODEL,
    instruction="""You are a story writer. Write a short story (around 100 words)""",
    include_contents='none',     # Do not include previous conversation context
    output_key="story",  # Key for storing output in session state
)

critic = Agent(
    name="Critic",
    model=GEMINI_MODEL,
    instruction=f"""You are a story critic. Review the story provided: {{story}}.
                   Provide 1-2 sentences of constructive criticism on how to improve it.
                   Focus on plot or character.

                   IF the document is coherent, addresses the topic adequately for its length,
                   and has no glaring errors or obvious omissions:
                   Respond *exactly* with the phrase "{COMPLETION_PHRASE}" and nothing else.
                   """,
    include_contents='none',  # Do not include previous conversation context
    output_key="criticism",   # Key for storing criticism in session state
)

reviser = Agent(
    name="Reviser",
    model=GEMINI_MODEL,
    instruction="""You are a story reviser. Revise the story provided: {story},
                   based on the criticism in {criticism}. Output only the revised story.""",
    include_contents='none',
    output_key="story",  # Overwrites the original story
)

tone_check = Agent(
    name="ToneCheck",
    model=GEMINI_MODEL,
    instruction="""You are a tone analyzer. Analyze the tone of the story provided: {story}.
                   Output only one word: 'positive' if the tone is generally positive,
                   'negative' if the tone is generally negative, or 'neutral' otherwise.""",
    include_contents='none',
    output_key="tone_check_result", # This agent's output determines the conditional flow
)