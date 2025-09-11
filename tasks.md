## T1. chat_agent
Google ADK를 사용해서 간단한 챗봇 에이전트를 만들어 보자.

1. chat_agent 폴더를 만든다.

2. agent.py 파일을 만들고 다음을 입력한다.
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.0-flash",
)
```
간단합니다. 이렇게 하면 Google ADK를 이용한 챗봇 완성입니다.

google.adk.agents 모듈에서 Agent 클래스를 import 한다.
chat_agent라는 이름의 agent이고, google gemini-2.0-flash 모델을 사용한다.
생성된 에이전트를 root_agent라는 변수에 저장한다.

---

3. __init__.py 파일을 만들고 다음을 입력한다.
```python
from . import agent
```
현재 폴더로부터 agent.py 모듈을 포함하라는 의미이다.
agent.py는 root_agent가 선언되어 있다.

이렇게 선언되면, 상위 폴더에서 chat_agent 모듈의 root_agent를 사용할 수 있다.

4. adk run으로 실행해 본다.
```shell
adk run chat_agent
```
console을 이용해서 chat_agent와 대화할 수 있다.

5. adk web으로 실행해 본다.
```
adk web --reload_agents
```
**--reload_agents** 옵션은 agent에 수정이 발생한 경우에 즉시 반영된다. 개발 시점에 좋다.

- 브라우저로 연결해서 확인할 수 있다.
- 간단한 대화를 해본다.
- 이벤트를 확인해 본다.
    - request에서 instruction과 content(이전 대화의 내용)을 확인할 수 있다.

6. instruction으로 persona를 설정해 본다.
```python
    instruction="너는 나의 친구야. 항상 편안한 말투로 대화해줘."
```
- 이벤트를 확인해 본다.
    - request의 instruction이 수정된 것을 알 수 있다.

## Gemini Models

- 다른 모델을 사용해 보자. gemini-2.5-flash
- New Session으로 새로운 대화 세션을 연다.
- gemini-2.5-flash만 하더라도 gemini-2.0-flash보다 성능이 좋은 것 같다.
- 원하는 결과에 적합한 모델을 선정하는 것도 중요하다.

## T2. math_agent
그럼 이번에는 4칙 연산 함수를 도구로 사용하는 math agent를 만들어 보자.

1. chat_agent 폴더를 복사해서 붙여 넣고, math_agent라고 폴더 이름을 바꿉니다.

2. chat_agent를 math_agent로 바꿉니다.

3. agent가 사용할 도구는 tools 파라미터로 전달합니다.
```python
    instruction="""4칙 연산 도구를 사용해서 사용자가 요청한 수식을 계산하고,
                   결과를 답하세요.""",
    tools=[add, subtract, multiply, divide],
```
4. instruction을 적어 봅니다. 어떤 상황에서 어떤 도구를 사용해야 하는지를 명확히 할수록 좋습니다. 4칙 연산이 명확하므로 이정도면 괜찮습니다.

5. 이제 add 등 에이전트가 사용할 도구를 선언해야 하는데, google adk에서는 일반 함수를 그대로 사용합니다.

```python
def add(a, b):
    return a + b
```

그런데, add라는 함수 이름으로 더한다는 것은 알 수 있겠지만, 에이전트가 이 함수를 제대로 사용하기 위해서는 이 함수에 대한 충분한 설명이 필요합니다. google adk에서는 docstring 주석을 사용합니다.

함수 선언 아래에 다음과 같은 주석을 삽입합니다.

```python
def add(a, b):
    """
    Adds two integers and returns the result.

    Args:
        a(int): The first integer.
        b(int): The second integer.

    Returns:
        int: The sum of the two integers
    """
    return a + b
```

6. subtract, multiply, divide 함수도 구현해 본다.

7. 실행해 본다.
- 처리 flow를 확인한다.
    - functionCall 이벤트 발생 -> functionResponse 이벤트 발생 -> AI Message 이벤트 발생.
- Request에 tools 항목을 보면 docstring으로 제공된 주석이 description으로 사용된 것을 확인할 수 있다.
    - LLM은 이를 근거로 함수를 호출해서 사용하게 된다.
    - LLM이 제대로 사용할 수 있도록 description을 잘 작성해야 한다.
    - 또한 instruction에도 어떤 상황에 도구를 사용해햐 할 지를 명확히 할 수록 좋다.

## T3. search_agent
이번에는 구글 검색을 이용하는 RAG 에이전트를 만들어 보자.
RAG는 Retrieval Augmented Generation으로 검색 결과를 근거로 답변하는 에이전트이다.

1. 구글 검색 도구를 도구로 제공하면 된다.

이미 adk에 google_search 도구가 제공된다.

```python
from google.adk.tools import google_search
```
```python
    tools=[google_search],
```

2. instruction은 어떻게 작성하면 될까?
```python
    instruction="사용자의 질문에 필요한 정보를 google_search 도구로 검색하고, 검색 결과를 근거로 답하세요.",
```

3. 좀 더 복잡한 요구를 해보자.
* 테슬라의 주가 현황에 대한 보고서를 만들어줘.
* 머스크가 최근에 개발자 없는 소프트웨어 회사를 만든다고 했는데, 어떤 내용인지 알려줘.

## ADK Runtime

* google adk는 event를 하나씩 처리하는 방식으로 동작합니다.
* 사용자의 요청을 수신한 Runner는 에이전트, 도구 등에게 처리를 요청하고, 이때 발생하는 Event를 Stream으로 사용자(App)에게 제공합니다.
* 대화 이력이 세션으로 관리되는데, session_service는 세션을 생성하고 관리한다.
* 대화 세션을 저장하는 것이 메모리이고, 문서나 이미지 같은 외부 데이터는 artifact로 관리한다.
* Runner는 이벤트를 근거로 세션, 메모리, artifact를 관리한다.

## T4. runner
* adk run, adk web 명령은 Runner를 생성하고 agent를 동작시킨다.
* python 명령으로 Runner를 구성해서 실행해 보자.

1. 사용자와의 대화를 구현해 보자.
* chat_agent에서 runner.py에 다음 코드를 추가한다.
    - 대화 새선을 생성해야 한다.
    - 사용자의 입력을 받아서, runner.run() 함수에 전달함으로써 에이전트와의 대화를 진행할 수 있다. 그런데, 이렇게 하면 안된다.
        - runner.run() 함수는 Generator를 반환한다.
```python
        session = await session_service.create_session(
                        app_name=root_agent.name, user_id="user1")

        user_input = input("User: ")
        event = runner.run(user_id=session.user_id, session_id=session.id, 
                           new_message=UserContent(user_input)):
```
---
* chat_agent에서 runner.py에 다음 코드를 추가한다.
    - async programming과 generator에 대해 설명한다.
    - 다음 내용을 추가해서 완성한다.
    - 실행해서 테스트 해 본다.
```python
        session = await session_service.create_session(
                        app_name=root_agent.name, user_id="user1")

        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit": break
            for event in runner.run(user_id=session.user_id, session_id=session.id, 
                                    new_message=UserContent(user_input)):
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")
```

2. 대화 종료 이후에 session에 저장된 event를 출력해 본다.
* chat_agent에서 runner.py에 다음 코드를 추가한다.
    - session에 저장된 events를 출력해 본다.
        - 그런데, 다음과 같이 하면 session.events가 출력되지 않는다.
        - session이 생성되면 session_service에 생성되고, 그와 복제된 것이 반환된다. DB 처럼.
        - session 정보가 필요하면 session_service에 다시 획득해야 한다. get_session 함수 이용.
```python
    print(session.events)
```
```python
    session = await session_service.get_session(app_name=session.app_name, user_id=session.user_id, session_id=session.id)
    print(session.events)
```
3. 이벤트를 확인해 본다.
* 사용자 대화 이벤트 --> 모델 대화 이벤트 --> ...

4. math 에이전트에 runner를 만들어서 동작해 본다.
* 이벤트를 확인해 보면, tool이 어떻게 사용되는지도 확인할 수 있다.
---
발표자료에서 시퀀스 다이어그램으로 설명한다.


## T5. country_agent
{country} 변수로 설정된 국가에 관한 질문에 답하는 Country 에이전트를 만들어 보자.
* session에 저장되는 state를 사용한다.

1. adk web에서 실행해 본다.
    - state에 country: 중국을 설정한 다음, 수도를 물어본다.
    - 이벤트에서 request.instruction을 확인해 본다.
    - state를 다시 일본으로 수정한 다음, 인구를 물어본다.
    - 이벤트에서 request.instruction을 확인해 본다.

2. runner를 만들어 보자.
    - session을 생성할 때, state를 설정한다.
```python
        print("궁금한 국가를 입력하세요. 'exit' 입력 시 종료됩니다.")
        while True:
            user_input = input("Country: ")
            if user_input.lower() == "exit": break
            session = await session_service.create_session(app_name=root_agent.name, 
                                    user_id="user1", state={"country": user_input})
```
---
LangChain과 ADK의 비교
Runner, SessionService, Session... 의 관계

ADK의 Agent 정의와 분류

## T6. country_agent with structured data
* LLM은 자연어 입출력을 제공한다.
    - structured format으로 입/출력을 받으려면 어떻게 해야 할까?
    - 가장 일반적인 방법은 json 포맷이다. instruction을 이렇게 수정해 보자.
```python
    instruction="""사용자는 {{"country": "한국"}}와 같은 JSON 형식으로 국가 이름을 제공합니다.
    요청된 국가의 수도를 {{"country": "한국", "capital": "서울"}} 형식의 JSON 객체로 응답하세요.""",
```
* 이렇게 출력된 json 포맷을 python dictionary로 해석해서 사용할 수 있다.
* pydantic 모듈을 사용해서 에이전트의 입출력 포맷을 설정할 수 있다.
    - pydantic 모듈은 구조체의 멤버 변수에 대해 type, description, constraint 등을 설정할 수 있다.
    - 따라서, LLM이 구조체를 어떻게 사용해야 하는지를 설명하는데에 활용된다.
```python
    import json
    json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)
```
* instruction이 없어도 잘 동작한다.
* instruction에서 구체적으로 input/output format을 명시하지 않아도 처리가 잘되는 것을 알 수 있다.
```python
    instruction="사용자가 요청한 국가에 대한 수도를 답변합니다."
```

## T7. code_agent
* BuiltInCodeExecutor를 사용하는 코딩 에이전트를 만들어 보자.
```python
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    name="code_agent", model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="파이썬 코드를 작성해서 주어진 문제를 해결하고 실행 결과를 출력하세요.",
    include_contents="none"
)
```

* 불필요한 설명 등이 포함된다면, instruction에 제약 사항을 명확히 한다.
```python
"최종 결과만 평문으로 반환하세요. 마크다운이나 코드 블록은 사용하지 마세요."
```
---
* Event의 content를 확인한다.
  - text 뿐만 아니라, executableCode, codeExecutionResult가 존재하는 것을 확인할 수 있다.

Workflow Agents
- SequentialAgent : sub_agents를 순차적으로 실행한다.
- ParallelAgent : sub_agents를 병렬적으로 실행한다.
- LoopAgent: sub_agents를 순차적으로 반복 실행한다.

## T8. story_agent
* sub_agents.py에 개별 에이전트를 만든다.
```python
    instruction="당신은 창의적인 글쓰기 도우미입니다. 요청에 맞는 짧은 이야기(2~4 문장)를 작성하세요.",
    instruction="""당신은 짧은 이야기 초안을 검토하는 건설적인 비평가입니다. 다음 이야기를 검토하고, 개선할 수 있는 명확하고 실행 가능한 방법이 있다면 그에 대한 구체적인 제안을 제공하세요.
    **검토할 이야기:**
    {story}
    **작업 가이드:**
    더 이상 개선할 사항이 없으면, *정확히* "No major issues found."라고 답하세요.
    """,
    instruction="""당신은 피드백을 기반으로 이야기를 다듬거나 프로세스를 종료하는 창의적인 글쓰기 도우미입니다.
    **이야기:**
    {story}
    **비평/제안:**
    {criticism}
    **작업 가이드:**
    비평이 *정확히* "No major issues found."라면, 'exit_loop' 함수를 호출하세요. 이 경우 추가 텍스트를 출력하지 마세요.
    그렇지 않으면, 비평에서 제안된 개선 사항을 신중하게 적용하여 이야기를 개선하세요.
    """,
```
* SequentialAgent와 LoopAgent로 story_agent를 완성한다.
```python
refiner_loop_agent = LoopAgent(name="loop", max_iterations=3,
                               sub_agents=[critic_agent, refiner_agent])
root_agent = SequentialAgent(name="sequential",
                             sub_agents=[initial_writer_agent, refiner_loop_agent])
```
---
* Custom Agent
    - Runner는 Agent의 run_async() 함수를 호출한다.
    - BaseAgent를 상속해서 확장하는 Agent는 _run_async_impl() 함수를 구현한다.
    - LLM을 사용하는 LlmAgent는 LLM flow의 run_async() 함수를 호출하고, 이는 event를 발생시킨다.

## T9. LambdaAgent
* 주어진 함수를 구동하는 함수 에이전트를 만들어 보자.
    - input_keys는 input parameter로 제공되는 state의 key 리스트이다.
    - output_key는 output이 저장되는 state의 key이다.
```python
        inputs = [ctx.session.state.get(k) for k in self.input_keys]
        output = self.func(*inputs)

        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=ModelContent(str(output)),
                    actions=EventActions(state_delta={self.output_key: output} if self.output_key else {}))
```
```python
        output = await self._maybe_await(self.func(*inputs))
        ...

    async def _maybe_await(self, value):
        if callable(getattr(value, "__await__", None)):
            return await value
        return value
```

## T10. JsonInputAgent
* JSON 입력을 state에 반영하는 에이전트를 만들어 보자.
```python
        text = ctx.user_content.parts[0].text if ctx.user_content and ctx.user_content.parts and ctx.user_content.parts[0].text else ""

        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=ctx.user_content,
                    actions=EventActions(state_delta=json.loads(text)))
```

## T11. calc_agent
* 주어진 숫자에 1을 더하고, 제곱한 결과를 반환하는 에이전트를 만들어 보자.

```python
from .json_input_agent import JsonInputAgent
from .lambda_agent import LambdaAgent

json_input_agent = JsonInputAgent(name="json_input_agent")
increase_agent = LambdaAgent(name="increase_agent", func=lambda x:x+1, input_keys=["number"], output_key="number")
sqaure_agent = LambdaAgent(name="increase_agent", func=lambda x:x*x, input_keys=["number"], output_key="number")

from google.adk.agents import SequentialAgent
root_agent = SequentialAgent(name="calc_agent",
             sub_agents=[json_input_agent, increase_agent, square_agent])
```

## T12. WhileAgent
* 조건을 만족하는 동안 반복 실행하는 While 에이전트를 만들어 보자.
* 먼저 LoopAgent의 구현에 대해 살펴보자.
    - 
```python
        running = True
        times_looped = 0
        while running and (not self.max_iterations or times_looped < self.max_iterations):
            times_looped += 1
            for agent in self.sub_agents:
                if running: running = eval(self.condition, {}, ctx.session.state)
                if not running: break
            
                async for event in agent.run_async(ctx):
                    yield event
                    if event.actions.escalate: running = False
```

## T13. fibonacci_agent
* WhileAgent를 사용해서 피보나치 값을 반환하는 에이전트를 만들어 보자.
    - 그림으로 그려보고, 에이전트마다 역할을 명확히 해보자.
```python
fibonacci_agent = SequentialAgent(name="fibonacci_agent",
                            sub_agents=[JsonInputAgent(name="json_input_agent"),
                                        WhileAgent(name="fibonacci_while_agent",
                                                   condition="len(sequence) <= number",
                                                   sub_agents=[LambdaAgent(name="fibonacci_sequence_agent",
                                                                           func=fibonacci,
                                                                           input_keys=["sequence"],
                                                                           output_key="sequence")]),
                                        LambdaAgent(name="fibonacci_output_agent",
                                                    func=lambda sequence, n: sequence[n],
                                                    input_keys=["sequence", "number"],
                                                    output_key="fibonacci_number")])

```

## T14. story_agent - custom workflow
* Custom 워크플로우를 가지는 Story 에이전트를 만들어 보자.
    - SequenceAgent나 LoopAgent를 사용하지 않고, 주어진 generator, critic, revisor 에이전트를 사용해서 story generation을 해본다.
```python
        running = True
        times_looped = 0
        while running and (not self.max_iterations or times_looped < self.max_iterations):
            times_looped += 1

            async for event in self.critic.run_async(ctx):
                yield event

            if ctx.session.state.get("criticism") == "No major issues found.":
                break

            async for event in self.reviser.run_async(ctx):
                yield event
```
---
Callbacks

## T15. memory_agent
* memory_service는 대화 세션을 저장하는 저장소 기능을 제공한다.
    - 현재 InMemoryMemoryService, VertexAiMemoryBankService, VertexAiRagMemoryService가 제공되고 있다.
* 이전 대화를 근거로 답하는 메모리 에이전트를 만들어 보자.
  - load_memory 도구를 사용한다.
* runner를 만들어 본다.
  - new가 입력되면 세션을 메모리에 저장하고, 새로운 세션을 시작한다.
```python
    session = await session_service.create_session(app_name=root_agent.name, user_id="user1")

    print("일상적인 대화를 나누는 에이전트입니다.")
    print("'new' 입력 시 새로운 대화가 시작됩니다. 'exit' 입력 시 종료됩니다.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit": break
        elif user_input.lower() == "new":
            session = await session_service.get_session(app_name=root_agent.name, user_id="user1", session_id=session.id)
            await memory_service.add_session_to_memory(session)

            session = await session_service.create_session(app_name=root_agent.name, user_id="user1")
        else:
            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
                if event.is_final_response(): print(f"Agent: {event.content.parts[0].text}")

```

## T16. image_agent using load_artifact
* artifact_service는 파일의 저장소 기능을 제공한다.
    - 현재 InMemoryArtifactService, Google Cloud Storage (GCS) MemoryService가 제공되고 있다.

## T17. date_agent
* 날짜와 요일에 대해 답하는 Date 에이전트를 만들어 보자.
    - get_today 함수를 사용한다.
* instruction에 get_today 함수 결과를 포함할 수도 있다.
```python
    instruction=f"사용자의 날짜와 요일에 관한 질문에 답하세요. 오늘은 {get_today()} 입니다.",
```
---
Define effective tool functions 


## T18. 
* LongRunningFunctionTool을 이용해서 Human-in-the-loop 구현해 보자.
    - LongRunningFunctionTool은 함수 response가 발생할 때, Event Generation이 종료된다.
    - 도구의 반환값을 확인해서, runner.run()을 호출해서 계속해야 한다.
    - session event를 출력해서 확인해 본다.

```python
    approval_request = None
    for event in runner.run(user_id=session.user_id, session_id=session.id,
                            new_message=UserContent(request)):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_response:
                    if part.function_response.name == "ask_for_approval":
                        approval_request = part.function_response
                elif part.text:
                    print(f"Agent: {part.text}")
```
```python
    if approval_request:
        result = input("Enter your response(approve or reject): ")
        approval_response = approval_request.model_copy(deep=True)
        approval_response.response["status"] = "approved" if result == "approve" else "rejected"

        for event in runner.run(user_id=session.user_id, session_id=session.id,
                                new_message=UserContent(parts=[Part(function_response=approval_response)])):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")
```
```python
    session = await session_service.get_session(app_name=session.app_name, user_id=session.user_id, session_id=session.id)
    print(session.events)
```
---
* tool behaviour를 설명한다.

## T19. summary_agent
* sub_agents
```python
    instruction="""당신은 유용한 도우미입니다.
        사용자가 텍스트 요약을 요청하면 'summarizer'에게 요청하세요.""",
    sub_agents=[summarizer],
```
* agent-as-a-tool
```python
from google.adk.tools import AgentTool

    instruction="""당신은 유용한 도우미입니다.
        사용자가 제공한 텍스트를 요약하기 위해 'summarizer' 도구를 사용하십시오""",
    tools=[AgentTool(agent=summarizer)],
```

---
* Agent-as-a-tool 과 sub-agent를 비교한다.

---
* built-in tools
* 3rd-party tools
---
* MCP
---
RAG & Vector DB

## T20. filesystem_agent

## T21. star collection
* EUCLIDean distance로 검색해 본다.
* COSINE, DOT으로 검색해 본다. --> 차이가 있다. 어떤 것이 적절할까?
    - 대부분 문서 검색에서는 COSINE distance를 사용한다.

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="star",
    vectors_config=VectorParams(size=2, distance=Distance.EUCLID),
                                               # Distance.COSINE, Distance.DOT
)

client.upsert(collection_name="star", points=points)
```
```python
near_points = client.query_points(
    collection_name="star",
    query=[2, 1],
    limit=3
)
print(near_points)
```

---
euclidean distance와 cosine distance에 대한 설명.
---
RAG의 개념

## T22. book_agent
* best-seller-books.json 파일에 대한 설명
    - 2024년 교보문고 베스트셀러 자료(1위~20위)
1. best-seller-books.json 파일을 읽어서 Qdrant DB에 저장한다.
    - vector를 생성해야 한다. 우선 description으로 vector를 생성해 보자.
    - 어떤 Embedding Model을 사용할 것인가.
---
* Hugging Face MTEB
    - Qwen3-Embedding-0.6B을 사용하자.
    - 다른 모델도 쉽게 테스트 해 볼 수 있다.

* 자 이제, best-seller-books.json 파일을 읽어서 Qdrant DB에 저장해 보자.
```python
import json
with open("best-seller-books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# pip install sentence-transformers hf_xet
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
# model = SentenceTransformer("Qwen/Qwen3-Embedding-4B")
# model = SentenceTransformer("BAAI/bge-m3")

from qdrant_client.models import PointStruct
points = [PointStruct(id=idx+1, vector=model.encode(book["description"]).tolist(),
                      payload=book) for idx, book in enumerate(books)]
```
```python
from qdrant_client import QdrantClient
client = QdrantClient()  # Connect to Qdrant (default: localhost:6333)
```
```python
from qdrant_client.models import VectorParams, Distance

collection_name="books"
client.create_collection(collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(),
    distance=Distance.COSINE)
)

client.upsert(collection_name=collection_name, points=points)
```
```python
near_points = client.query_points(
    collection_name="books",
    query=model.encode("""역사와 인간의 본질을 다룬 충격적이고 도발적이라고 평가된
                          한강의 소설에 대해 알려줘""").tolist(),
    limit=3
)

for point in near_points.points:
    print(point.payload['title'], point.payload['author'], point.score)
```

2. book_agent를 완성해 보자.
* book_agent가 사용할 도구를 정의한다.

```python
def get_best_sellers(query: str, top_k: int = 3):
    """
    주어진 쿼리에 대해 벡터 유사도 검색을 통해 책을 찾아서 반환합니다.

    Args:
        query (str): 검색할 쿼리 문자열
        top_k (int): 반환할 상위 k개의 책 수 (기본값: 3)

    Returns:
        List[dict]: 검색된 책의 리스트, 각 책은 딕셔너리 형태로 반환됩니다.
    """
    near_points = client.query_points(
        collection_name="books",
        query=model.encode(query).tolist(),
        limit=top_k
    )

    return [point.payload for point in near_points.points]
```
```python
root_agent = Agent(
    name="book_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 베스트셀러에 관한 질문에 답하세요.",
    tools=[get_best_sellers]
)
```

3. filter를 이용해 보자.
```python
near_points = client.query_points(
    collection_name="books",
    query=model.encode("""역사와 인간의 본질을 다룬 소설에 대해 알려줘""").tolist(),
    query_filter=Filter(
        must=[FieldCondition(key="author", match=MatchValue(value="한강"))]
    ),
    limit=3
)
```
* filter도 LLM이 설정하도록 해야 한다.
    - json 문자열로 제공되는 필터 조건으로부터 Qdrant Filter를 생성해서 처리해야 한다.

```python
def search_books(query: str, filter: dict = None, top_k: int = 3):
    """주어진 쿼리에 대해 벡터 유사도 검색을 통해 책을 찾아서 반환합니다.
    필터 조건이 주어지면 해당 조건에 맞는 책만 검색합니다.

    Args:
        query (str): 검색할 쿼리 문자열
        filter (dict): 필터 조건 (예: {"author": "한강"})
        top_k (int): 반환할 상위 k개의 책 수 (기본값: 3)

    Returns:
        List[dict]: 검색된 책의 리스트, 각 책은 딕셔너리 형태로 반환됩니다.
    """
    near_points = client.query_points(
        collection_name="books",
        query=model.encode(query).tolist(),
        query_filter=_parse_filter(filter),
        limit=top_k
    )
```
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range, MatchText
def _parse_filter(filters: dict):
    """
    filter dict를 Qdrant Filter must 조건 리스트로 변환.
    지원 operator: eq, ne, gt, lt, gte, lte

    Args:
        filter (dict): 필터 조건 (예: {"author": "한강"})

    Returns:
        Filter: Qdrant의 Filter 객체
    """
    must_conditions = []
    should_conditions = []
    must_not_conditions = []

    for key, cond in filters.items():
        # 단순 eq: {"author": "한강"}
        if not isinstance(cond, dict):
            must_conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(value=cond)
                )
            )
            continue

        # operator 방식: {"author": {"ne": "한강"}}
        for op, value in cond.items():
            if op == "eq":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            elif op == "ne":
                must_not_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            elif op == "gt":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(gt=value)
                    )
                )
            elif op == "lt":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(lt=value)
                    )
                )
            elif op == "gte":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(gte=value)
                    )
                )
            elif op == "lte":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        range=Range(lte=value)
                    )
                )
            # 텍스트 검색 지원 (예시)
            elif op == "text":
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchText(text=value)
                    )
                )
            # 기타 연산자 필요시 추가

    return Filter(
        must=must_conditions if must_conditions else None,
        must_not=must_not_conditions if must_not_conditions else None,
        should=should_conditions if should_conditions else None
    )
```

* 추가적인 개선 포인트는?