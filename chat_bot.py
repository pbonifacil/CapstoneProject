"""
ChatBot class
"""

from openai import OpenAI


class GPT_Engine:
    def __init__(self,
                 OPENAI_API_KEY: str,
                 system_behavior: str = "",
                 model="gpt-3.5-turbo",
                 ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    def get_completion(self, prompt, temperature=0):
        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )

        self.messages.append(
            {"role": "assistant",
             "content": completion.choices[0].message.content}
        )

        return completion.choices[0].message.content


class CarChatBot:
    """
    Generate a response by using LLMs.
    """

    def __init__(self, system_behavior: str, api_key: str):
        self.__system_behavior = system_behavior

        self.engine = GPT_Engine(
            OPENAI_API_KEY=api_key,
            system_behavior=system_behavior
        )

    def generate_response(self, message: str):
        return self.engine.get_completion(message)

    def __str__(self):
        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        return f"🤖 {class_name}."

    def reset(self):
        ...

    @property
    def memory(self):
        return self.engine.messages

    @property
    def system_behavior(self):
        return self.__system_behavior

    @system_behavior.setter
    def system_behavior(self, system_config: str):
        self.__system_behavior = system_config

