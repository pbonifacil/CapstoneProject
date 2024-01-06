import streamlit as st
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from webpage import home, account, chatbot, policies, contacts


st.set_page_config(page_title='AutoMentor', page_icon='🏁', layout='wide')


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():

        with st.sidebar:
            st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {
                    width: 333px !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
            )

            app = option_menu(
                menu_title='🚘 AutoMentor 🚘',
                options=['Home', 'Account', 'Chatbot', 'Policies', 'Contacts'],
                icons=['house', 'person', 'robot', 'receipt', 'telephone'],
                menu_icon=' ',
                default_index=0
            )

        if app == 'Home':
            home.app()
        if app == 'Account':
            account.app()
        if app == 'Chatbot':
            chatbot.app()
        if app == 'Policies':
            policies.app()
        if app == 'Contacts':
            contacts.app()

    run()
