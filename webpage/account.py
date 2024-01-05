import streamlit as st
from chatbot_util.login import login_signup


def app():
    st.title('Account')
    if not st.session_state.get("logged_in", False):
        login_signup()
        st.stop()
    else:
        with st.sidebar:
            st.success("🔓 Logged in as " + st.session_state["user_data"]["Username"])
