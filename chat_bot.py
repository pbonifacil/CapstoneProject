"""
ChatBot class
"""

from openai import OpenAI


class GPT_Helper:
    def __init__(self, OPENAI_API_KEY):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

        return completion.choices[0].message.content


class ChatBotGPT:
    """
    Generate a response by using LLMs.
    """

    def __init__(self, engine):
        self.memory = []
        self.engine = engine

    def generate_response(self, message: str):
        return self.engine.get_completion(message)
