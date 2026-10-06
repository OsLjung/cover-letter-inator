import yaml
from openai import OpenAI

class Agent:
    def __init__(self, name):
        self.name = name

        self.api_key = None
        with open('config.yaml', 'r') as file:
            configs = yaml.safe_load(file)
            with open(configs.get('apiKeyPath', None), 'r') as key_file:
                self.api_key = key_file.read().strip()

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
            )
    def generate_response(self, user_input):
        # First API call with reasoning
        response = self.client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )
        # Extract the assistant message with reasoning_details

        # Preserve the assistant message with reasoning_details
        messages = [
            {"role": "user", "content": user_input},
            {
                "role": "assistant",
                "content": response.content,
                "reasoning_details": response.reasoning_details  # Pass back unmodified
            },
            {"role": "user", "content": "Are you sure? Think carefully."}
        ]
        #second api call.
        response2 = self.client.chat.compleations.create(

            model="openrouter/free",
            messages=messages,
        )

        return response2.choices[0].message.content
if __name__ == "__main__":
    agent = Agent("MyAgent")
    print(agent.generate_response('this is a test, please respond with a with the names of all the ninja turtles'))
