from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import story_agent

GEMINI_MODEL = "gemini-2.0-flash"

def exit_loop(tool_context: ToolContext):
  """더 이상 수정할 사항이 없는 경우에 반복 프로세스를 종료하도록 신호를 보내는 함수입니다."""
  tool_context.actions.escalate = True
  return {}     # Return empty dict

initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    description="짧은 이야기를 작성하는 에이전트.",
    instruction=f"당신은 창의적인 글쓰기 도우미입니다. 요청에 맞는 짧은 이야기(2~4 문장)를 작성하세요.",
    output_key="story"
)

critic_agent = Agent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    description="이야기를 검토하고 개선할 수 있는 방법을 제안하는 에이전트.",
    instruction=f"""당신은 짧은 이야기 초안을 검토하는 건설적인 비평가입니다. 다음 이야기를 검토하고, 개선할 수 있는 명확하고 실행 가능한 방법이 있다면 그에 대한 구체적인 제안을 제공하세요.
    **검토할 이야기:**
    ```
    {{story}}
    ```

    **작업 가이드:**
    문서의 명확성, 몰입도 및 기본적인 일관성을 검토합니다.
    독자의 몰입도를 높이기 위한 명확한 방안이 있으면 1-2가지 제안하세요. 예: "더 강력한 도입 문장이 필요하다", "캐릭터의 목표를 명확히 하라".
    구체적이고 간결한 제안을 제공하세요. 더 이상 수정할 사항이 없다면 *정확히* "No major issues found."라는 문구를 정확히 출력하세요.
    비평 내용만 출력하고 추가 설명은 하지 마세요.
    """,
    output_key="criticism",
)


refiner_agent = Agent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    # Relies solely on state via placeholders
    include_contents='none',
    description="비평/제안에 따라 이야기를 다듬거나 프로세스를 종료하는 에이전트.",
    instruction=f"""당신은 피드백을 기반으로 이야기를 다듬거나 프로세스를 종료하는 창의적인 글쓰기 도우미입니다.
    **이야기:**
    ```
    {{story}}
    ```
    **비평/제안:**
    {{criticism}}

    **작업 가이드:**
    '비평/제안'을 분석합니다. 비평이 *정확히* "No major issues found."라면, 'exit_loop' 함수를 호출하세요. 이 경우 추가 텍스트를 출력하지 마세요.
    그렇지 않으면, 비평에서 제안된 개선 사항을 신중하게 적용하여 이야기를 개선하세요. 개선된 문서만 출력하고, 'exit_loop' 함수를 호출하지 마세요.
    """,
    tools=[exit_loop], # Provide the exit_loop tool
    output_key="story"
)

from typing_extensions import override
from typing import AsyncGenerator, Optional
from google.adk.agents import Agent, BaseAgent, InvocationContext
from google.adk.events import Event

class StoryAgent(BaseAgent):
    """
    Story generating agent to orchestrate the story creation process.
    """
    # --- Field Declarations for Pydantic ---
    # Declare the agents passed during initialization as class attributes with type hints
    generator: Agent
    critic: Agent
    reviser: Agent

    max_iterations: Optional[int] = None

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Generate the initial story
        async for event in self.generator.run_async(ctx):
            yield event

        running = True
        times_looped = 0
        while running and (not self.max_iterations or times_looped < self.max_iterations):
            times_looped += 1

            # Generate criticism
            async for event in self.critic.run_async(ctx):
                yield event

            if ctx.session.state.get("criticism", "No major issues found.") == "No major issues found.":
                # If no major issues found, exit the loop
                break

            # Generate revision
            async for event in self.reviser.run_async(ctx):
                yield event

story_agent = StoryAgent(
    name="StoryAgent",
    generator=initial_writer_agent,
    critic=critic_agent,
    reviser=refiner_agent,
    max_iterations=5  # Limit loops to prevent infinite loops
)