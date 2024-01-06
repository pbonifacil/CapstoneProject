import re

CUSTOMER_DATA_PATH = "webpage/chatbot_util/customer_data.csv"
DATASET_PATH = "webpage/chatbot_util/car_dataset.csv"


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
    selected_columns = ['Brand', 'Model', 'Fuel', 'Year', 'Kilometers', 'Power_hp', 'Color', 'Condition', 'Price_EUR']
    selected_rows = df.loc[index_list][selected_columns]
    selected_rows.columns = ['Brand', 'Model', 'Fuel', 'Year', 'Kilometers', 'Power (hp)', 'Color', 'Condition',
                             'Price (€)']

    # Convert the selected rows to a Markdown table
    markdown_table = selected_rows.to_markdown()

    # Merge 'Brand' and 'Model' into a single column 'Car' in the photo DataFrame
    photo_df = df.loc[index_list][['Brand', 'Model', 'Photo']]
    photo_df['Car'] = '#' + photo_df.index.astype(str) + ' ' + photo_df['Brand'] + ' ' + photo_df['Model']

    photo_df = photo_df[['Car', 'Photo']].reset_index(drop=True)

    return markdown_table, photo_df


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
