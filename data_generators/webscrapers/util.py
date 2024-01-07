from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def get_completion(prompt, temperature=0, messages=[], model="gpt-3.5-turbo",
                   client=OpenAI()):
    message = {"role": "user", "content": prompt}

    messages.append(message)

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    return completion.choices[0].message.content
