import re

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


def extract_listing_ids(input_string):
    # Use regular expression to find all numbers inside square brackets
    numbers_inside_brackets = re.findall(r'\[([\d\s,]+)\]', input_string)

    if not numbers_inside_brackets:
        return None, input_string

    # Extract and split the numbers inside square brackets
    extracted_numbers = [int(num) for num in numbers_inside_brackets[0].split(',')]

    # Remove everything inside square brackets from the input string
    output_string = re.sub(r'\[.*?\]', '', input_string)

    return extracted_numbers, output_string.strip()


def generate_markdown_table(df, index_list):
    # Select rows based on the given indices
    selected_columns = ['Brand', 'Model', 'Price_EUR', 'Year', 'Kilometers', 'Fuel', 'Gear_Type', 'Condition']
    selected_rows = df.loc[index_list][selected_columns]

    # Convert the selected rows to a Markdown table
    markdown_table = selected_rows.to_markdown()

    return markdown_table


def format_assistant_response(input_string, df):
    # Extract the listing ids from the input string
    listing_ids, input_string = extract_listing_ids(input_string)

    if listing_ids:
        # Generate a Markdown table with the selected listings
        markdown_table = generate_markdown_table(df, listing_ids)

        # Format the assistant response
        assistant_table = f"\n\n{markdown_table}"
        return assistant_table
    else:
        return input_string
