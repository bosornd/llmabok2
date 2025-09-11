from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    name="code_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="""주어진 문제를 해결하기 위해 파이썬 코드를 작성하고 실행한 결과를 출력하세요.
                   최종 결과만 평문으로 반환하세요. 마크다운이나 코드 블록은 사용하지 마세요.""",
    include_contents='none'
)