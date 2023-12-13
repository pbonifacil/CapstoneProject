import time
import streamlit as st
from agent import CarDealerChatbot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def initialize() -> None:
    """
    Initialize the app
    """
    st.set_page_config(layout='centered', page_title='AutoMentor')
    page_bg_img = '''
        <style>
        [data-testid="ScrollToBottomContainer"] {
        background-image: url("https://i.imgur.com/1PBP7xR.png");
        background-size: cover;
        }
        .stChatFloatingInputContainer {
                background-color: rgba(0, 0, 0, 0)
        }
        [data-testid="stHeader"] {
                background-color: rgba(0, 0, 0, 0)
        }
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("AutoMentor")

    st.sidebar.title("🤖")

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CarDealerChatbot(path="webscrapers/car_dataset_small.csv")

    with st.sidebar:
        st.markdown(
            f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
        )


def display_history_messages():
    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.agent.memory.chat_memory.messages:
        if message.__class__.__name__ == "AIMessage":
            role = "assistant"
            avatar = "🤖"
        else:
            role = "user"
            avatar = "😎"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.content)


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    with st.chat_message("user", avatar="😎"):
        st.markdown(message)


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_assistant_msg(message: str):
    """
    Display assistant message
    """
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()

        # Simulate stream of response with milliseconds delay
        full_response = ""
        for chunk in message.split():
            full_response += chunk + " "
            time.sleep(0.02)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)


# [*]                                                                                            #
# [*] MAIN                                                                                       #
# [*]                                                                                            #

if __name__ == "__main__":
    initialize()

    # [i] Display History #
    display_history_messages()

    if prompt := st.chat_input("Type your request..."):
        # [*] Request & Response #
        display_user_msg(message=prompt)
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt
        )
        display_assistant_msg(message=assistant_response['output'])

    # [i] Sidebar #
    with st.sidebar:
        with st.expander("Information"):
            st.text("💬 MEMORY")
            st.write(st.session_state.chatbot.agent.memory.chat_memory.messages)
