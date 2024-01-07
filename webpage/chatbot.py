import time
import streamlit as st
from langchain_core.messages import AIMessage

from webpage.chatbot_util.agent import AutoMentorChatbot
from webpage.chatbot_util.login import login_signup
from webpage.chatbot_util.util import extract_listing_ids, generate_markdown_table


# TODO: vector database / valueerror no predict

def initialize() -> None:
    """
    Initialize the app
    """
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

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = AutoMentorChatbot(conversation_preferences=st.session_state['user_data'][
                                                         'Bot Preferences'])

    with st.sidebar:
        st.markdown(
            f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
        )

    st.success(f"👋 Welcome back, {st.session_state['user_data']['Full Name']}!")


def display_history_messages():
    # Display chat messages from history on app rerun
    avatar_dict = {'assistant': '🤖', 'user': '😎'}
    for message in st.session_state.chatbot.chat_history:
        if message['role'] == 'assistant':
            listing_ids, clean_message = extract_listing_ids(message['content'])
            with st.chat_message(message['role'], avatar=avatar_dict[message['role']]):
                st.markdown(clean_message)
                if listing_ids:
                    table, photo_df = generate_markdown_table(st.session_state.chatbot.agent.tools[0].locals['df'],
                                                              listing_ids)
                    st.markdown(f"\n\n{table}")
                    st.markdown("")
                    st.markdown("\n\nHere are the corresponding photos:\n\n")
                    num_images = len(photo_df)
                    columns = st.columns(5)
                    for i in range(num_images):
                        with columns[i]:
                            if photo_df['Photo'][i] == 'Não disponível':
                                st.markdown(f"\n\n🚫 Photo not available\n\n\n{photo_df['Car'][i]}")
                                continue
                            st.image(photo_df['Photo'][i], caption=photo_df['Car'][i], width=200)

                    st.markdown("")
                    st.markdown(
                        "If you would like more information about a particular car, please specify the corresponding car number 😊.")
        else:
            with st.chat_message(message['role'], avatar=avatar_dict[message['role']]):
                st.markdown(message['content'])


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    with st.chat_message("user", avatar="😎"):
        st.markdown(message)
    st.session_state.chatbot.chat_history.append({"role": "user", "content": message})


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def simulate_typing(message: str):
    """
    Simulate typing
    """
    message_placeholder = st.empty()

    # Simulate stream of response with milliseconds delay
    for i in range(len(message)):
        time.sleep(0.02)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(message[:i] + "▌")

    message_placeholder.markdown(message)


def display_assistant_msg(message: str):
    """
    Display assistant message
    """
    listing_ids, clean_message = extract_listing_ids(message)

    with st.chat_message("assistant", avatar="🤖"):
        simulate_typing(clean_message)

        if listing_ids:
            table, photo_df = generate_markdown_table(st.session_state.chatbot.agent.tools[0].locals['df'], listing_ids)
            st.markdown(f"\n\n{table}")
            st.markdown("")
            st.markdown("\n\nHere are the corresponding photos:\n\n")
            num_images = len(photo_df)
            columns = st.columns(5)
            for i in range(num_images):
                with columns[i]:
                    if photo_df['Photo'][i] == 'Não disponível':
                        st.markdown(f"\n\n🚫 Photo not available\n\n\n{photo_df['Car'][i]}")
                        continue
                    st.image(photo_df['Photo'][i], caption=photo_df['Car'][i], width=200)

            st.markdown("")
            more_info = "If you would like more information about a particular car, please specify the corresponding car number 😊."
            simulate_typing(more_info)
            message += more_info

    st.session_state.chatbot.chat_history.append({"role": "assistant", "content": message})


def greeting():
    """
    Greeting message
    """
    greeting = f"Greetings {st.session_state['user_data']['Full Name'].split()[0]}! I'm AutoMentor, your dedicated automotive assistant. Whether you're searching for the perfect car listing or looking to appraise the value of a vehicle you're considering selling, I'm here to assist. What can I do for you today?"
    display_assistant_msg(message=greeting)
    st.session_state.chatbot.agent_memory.append(AIMessage(content=greeting))


# [*]                                                                                            #
# [*] MAIN                                                                                       #
# [*]                                                                                            #

def app():
    st.caption('🤖 | Chatbot')
    st.write('---')

    # [i] Login #
    if not st.session_state.get("logged_in", False):
        login_signup()
        st.stop()
    else:
        with st.sidebar:
            st.success("🔓 Logged in as " + st.session_state["user_data"]["Username"])

    # st.session_state['user_data'] = {'Full Name': 'Pedro Bonifacio', 'Age': 22,
    #                                  'Location': 'Lisbon', 'Favorites': [],
    #                                  'Bot Preferences': 'Talk like a butler'}

    initialize()
    display_history_messages()
    if not st.session_state.chatbot.chat_history:
        st.chat_input("Loading...")
        greeting()

    if prompt := st.chat_input("Type your request..."):
        # [*] Request & Response #
        display_user_msg(message=prompt)
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt
        )

        display_assistant_msg(message=assistant_response)

    # [i] Sidebar #
    with st.sidebar:
        with st.expander("💬 CHAT HISTORY"):
            st.write(st.session_state.chatbot.chat_history)
        with st.expander("💬 AGENT MEMORY"):
            st.write(st.session_state.chatbot.agent_memory)
