import streamlit as st
from webpages.chatbot_util.login import login_signup
import pandas as pd
from webpages.chatbot_util.util import CUSTOMER_DATA_PATH


def app():
    st.caption('😎 | Account')
    st.write('---')

    if not st.session_state.get("logged_in", False):
        login_signup()
        st.stop()
    else:
        with st.sidebar:
            st.success("🔓 Logged in as " + st.session_state["user_data"]["Username"])

    user_data = st.session_state["user_data"]

    if not st.session_state.get("editing_info", False):
        for key, value in user_data.items():
            st.write(f"**{key}:**   {value}")
    else:
        st.subheader("Edit Information")

        # Create input fields with default values set to current user data
        edited_data = {}
        for key, value in user_data.items():
            edited_data[key] = st.text_input(f"Enter {key}:", value)
        new_password = st.text_input("Enter new password (leave empty if you don't want to change):", type="password")

        # Save the edited data
        if st.button("Save Changes"):
            if isinstance(new_password, str):
                save_data(edited_data, new_password)
            else:
                save_data(edited_data, None)
            st.session_state["user_data"] = edited_data
            st.session_state["editing_info"] = False
            st.rerun()

    # Edit Info button
    if st.button("Edit Info"):
        st.session_state["editing_info"] = True
        st.rerun()


def save_data(user_data, new_password):
    """Save the user data to the CSV file."""
    user_data['Age'] = int(user_data['Age'])

    customer_data = pd.read_csv(CUSTOMER_DATA_PATH)

    index_to_update = customer_data.index[customer_data['Username'] == st.session_state['user_data']['Username']][0]

    old_record = customer_data.loc[index_to_update].copy()

    if new_password:
        user_data['Password'] = new_password
    else:
        user_data['Password'] = old_record['Password']

    # Change all values in the row to the new values except for the 'Password' column
    for key, value in user_data.items():
        old_record.loc[key] = value

    # Update the original DataFrame with the modified row
    customer_data.loc[index_to_update] = old_record

    # Save the updated DataFrame to a new CSV file
    customer_data.to_csv(CUSTOMER_DATA_PATH, index=False)
    del user_data['Password']