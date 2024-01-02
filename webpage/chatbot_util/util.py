from openai import OpenAI, AuthenticationError


def is_valid_api_key(api_key):
    messages = [{"role": "user", "content": "Hello!"}]

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        return True
    except AuthenticationError as e:
        return False
