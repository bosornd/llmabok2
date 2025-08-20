from google.adk.agents import SequentialAgent, ParallelAgent
from .json_input_agent import JsonInputAgent
from .lambda_agent import LambdaAgent
from .while_agent import WhileAgent

# simle calculator agent
increase_agent = LambdaAgent(name="increase_agent",
                             func=lambda x: x + 1,
                             input_keys=["number"],
                             output_key="number")

square_agent = LambdaAgent(name="square_agent",
                           func=lambda x: x ** 2,
                           input_keys=["number"],
                           output_key="number")

calc_agent = SequentialAgent(name="calc_agent",
                            sub_agents=[JsonInputAgent(name="json_input_agent"),
                                        increase_agent,
                                        square_agent])

# fibonacci agent
def fibonacci(f: list[int]) -> list[int]:
    """
    Generate the next Fibonacci number in the sequence.
    """
    if f is None: f = [0, 1]
    f.append(f[-1] + f[-2])
    return f

fibonacci_agent = SequentialAgent(name="fibonacci_agent",
                            sub_agents=[JsonInputAgent(name="json_input_agent"),
                                        WhileAgent(name="fibonacci_while_agent",
                                                   condition="len(sequence) <= number",
                                                   sub_agents=[LambdaAgent(name="fibonacci_sequence_agent",
                                                                           func=fibonacci,
                                                                           input_keys=["sequence"],
                                                                           output_key="sequence")]),
                                        LambdaAgent(name="fibonacci_output_agent",
                                                    func=lambda sequence, n: f"{sequence[n]}",
                                                    input_keys=["sequence", "number"],
                                                    output_key="fibonacci_number")])

# root_agent = calc_agent
root_agent = fibonacci_agent