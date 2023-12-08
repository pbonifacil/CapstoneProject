from streamlit import secrets
from openai import OpenAI


def get_completion(prompt, temperature=0, messages=[], model="gpt-3.5-turbo",
                   client=OpenAI(api_key=secrets['OPENAI_API_KEY'])):
    message = {"role": "user", "content": prompt}

    messages.append(message)

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    return completion.choices[0].message.content
