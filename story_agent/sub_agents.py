from google.adk.agents import Agent
from google.adk.tools import exit_loop

GEMINI_MODEL = "gemini-2.0-flash"

initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=GEMINI_MODEL,
    output_key="story",
    instruction="당신은 창의적인 글쓰기 도우미입니다. 요청에 맞는 짧은 이야기(2~4 문장)를 작성하세요.",
)

critic_agent = Agent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    output_key="criticism",
    instruction="""당신은 짧은 이야기 초안을 검토하는 건설적인 비평가입니다. 다음 이야기를 검토하고, 개선할 수 있는 명확하고 실행 가능한 방법이 있다면 그에 대한 구체적인 제안을 제공하세요.
    **검토할 이야기:**
    {story}
    **작업 가이드:**
    더 이상 개선할 사항이 없으면, *정확히* "No major issues found."라고 답하세요.
    """,
)

refiner_agent = Agent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    output_key="story",
    tools=[exit_loop],
    instruction="""당신은 피드백을 기반으로 이야기를 다듬거나 프로세스를 종료하는 창의적인 글쓰기 도우미입니다.
    **이야기:**
    {story}
    **비평/제안:**
    {criticism}
    **작업 가이드:**
    비평이 *정확히* "No major issues found."라면, 'exit_loop' 함수를 호출하세요. 이 경우 추가 텍스트를 출력하지 마세요.
    그렇지 않으면, 비평에서 제안된 개선 사항을 신중하게 적용하여 이야기를 개선하세요.
    """,
)
