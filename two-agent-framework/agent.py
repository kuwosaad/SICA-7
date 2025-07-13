import os
from openai import OpenAI

class Agent:
    def __init__(self, name, model="openai/gpt-3.5-turbo"):
        self.name = name
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.messages = []

    def send_message(self, recipient_agent, message_content):
        print(f"\n{self.name} sending message to {recipient_agent.name}: {message_content}")
        self.messages.append({"role": "user", "content": message_content})
        recipient_agent.receive_message(self, message_content)

    def receive_message(self, sender_agent, message_content):
        print(f"{self.name} received message from {sender_agent.name}.")
        self.messages.append({"role": "assistant", "content": message_content})
        # In a real scenario, the agent would process this message and generate a response.
        # For now, we'll just acknowledge receipt.

    def generate_response(self):
        if not self.messages:
            return "No messages to respond to."

        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=False,
            )
            response_content = chat_completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_content})
            return response_content
        except Exception as e:
            return f"Error generating response: {e}"

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
