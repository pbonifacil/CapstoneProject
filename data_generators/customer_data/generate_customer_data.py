import pandas as pd
import random


# Function to generate email from username
def generate_email(username):
    return f"{username.lower()}@example.com"


def generate_username(first_name, last_name):
    return f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"


def generate_password():
    password_length = random.randint(5, 7)
    password = ''.join(
        random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(password_length))
    return password


# Generate fictional customer data for 150 customers
num_customers = 150
first_names = ['John', 'Jane', 'Mike', 'Emily', 'Chris', 'David', 'Sarah', 'Daniel', 'Olivia', 'William']
last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']

customer_data = {
    'Email': [],
    'Full Name': [],
    'Username': [],
    'Password': [generate_password() for _ in range(num_customers)],
    'Age': [random.randint(18, 70) for _ in range(num_customers)],
    'Location': [random.choice(['Lisboa', 'Coimbra', 'Porto', 'Albufeira', 'Aveiro']) for _ in
                 range(num_customers)],
    'Bot Preferences': [random.choice(
        ['Talk like a butler', 'Talk like Top Gear\'s Richard Hammond', 'Talk like a car salesman',
         'Talk like Top Gear\'s Jeremy Clarkson', 'Talk like a car expert']) for _ in range(num_customers)]
}

for _ in range(num_customers):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    username = generate_username(first_name, last_name)
    customer_data['Email'].append(generate_email(username))
    customer_data['Full Name'].append(full_name)
    customer_data['Username'].append(username)

# Create a DataFrame
customer_df = pd.DataFrame(customer_data)

# Save DataFrame to CSV
customer_df.to_csv('customer_data.csv', index=False)
