import time
import streamlit as st
from chat_bot import GPT_Helper, ChatBotGPT
from util import local_settings


def initialize() -> None:
    """
    Initialize the app
    """
    st.title("AutoMentor")

    if "chatbot" not in st.session_state:
        gpt = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY)
        st.session_state.chatbot = ChatBotGPT(engine=gpt)


def display_history_messages():
    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    st.session_state.chatbot.memory.append(
        {"role": "user", "content": message}
    )

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
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

        st.session_state.chatbot.memory.append(
            {"role": "assistant", "content": full_response}
        )


# [*]                                                                                            #
# [*] MAIN                                                                                       #
# [*]                                                                                            #

if __name__ == "__main__":
    page_bg_img = '''
    <style>
    [data-testid="ScrollToBottomContainer"] {
    background-image: url("https://images.hdqwalls.com/download/retrowave-car-4k-fr-1920x1080.jpg");
    background-size: cover;
    }
    .stChatFloatingInputContainer {
            bottom: 20px;
            background-color: rgba(0, 0, 0, 0)
    }
    
    [data-testid="stHeader"] {
            bottom: 20px;
            background-color: rgba(0, 0, 0, 0)
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    initialize()

    # [i] Display History #
    display_history_messages()

    if prompt := st.chat_input("Type your request..."):
        # [*] Request & Response #
        display_user_msg(message=prompt)
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt
        )
        display_assistant_msg(message=assistant_response)

    # [i] Sidebar #
    with st.sidebar:
        st.write(st.session_state.chatbot.memory)
