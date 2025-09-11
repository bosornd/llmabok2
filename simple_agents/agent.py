from google.adk.agents import SequentialAgent

from .json_input_agent import JsonInputAgent
from .lambda_agent import LambdaAgent
from .while_agent import WhileAgent

# fibonacci agent
from typing import Optional
def fibonacci(f: Optional[list[int]]) -> list[int]:
    """
    Generate the next Fibonacci number in the sequence.
    """
    if f is None: f = [0, 1]
    f.append(f[-1] + f[-2])
    return f

fibonacci_agent = SequentialAgent(name="fibonacci_agent",
                            sub_agents=[JsonInputAgent(name="json_input_agent"),
                                        WhileAgent(name="fibonacci_while_agent",
                                                   condition="'sequence' not in locals() or len(sequence) <= number",
                                                   sub_agents=[LambdaAgent(name="fibonacci_sequence_agent",
                                                                           func=fibonacci,
                                                                           input_keys=["sequence"],
                                                                           output_key="sequence")]),
                                        LambdaAgent(name="fibonacci_output_agent",
                                                    func=lambda sequence, n: sequence[n],
                                                    input_keys=["sequence", "number"],
                                                    output_key="fibonacci_number")])

# root_agent = calc_agent
root_agent = fibonacci_agent