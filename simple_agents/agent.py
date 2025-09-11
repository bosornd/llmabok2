from .lambda_agent import LambdaAgent

root_agent = LambdaAgent(name="increase_agent",
                         func=lambda x: x + 1,
                         input_keys=["number"],
                         output_key="number")
