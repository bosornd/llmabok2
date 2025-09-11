from google.adk.agents import Agent

from datetime import datetime
def get_today() -> str:
    """
    오늘의 날짜와 요일을 반환합니다.
    """
    return datetime.now().strftime("%Y-%m-%d %A")

root_agent = Agent(
    name="date_agent",
    model="gemini-2.0-flash",
    instruction=f"사용자의 날짜와 요일에 관한 질문에 답하세요. 오늘 날짜와 요일은 {get_today()}입니다.",
)

root_agent = Agent(
    name="date_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 날짜와 요일에 관한 질문에 답하세요. 오늘 날짜와 요일은 'get_today()' 함수로 알 수 있습니다.",
    tools=[get_today],
)
