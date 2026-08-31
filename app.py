import streamlit as st
import requests


# -----------------------------
# App title
# -----------------------------

st.title("My AI Chatbot 🤖")


# -----------------------------
# Sidebar Settings
# -----------------------------

st.sidebar.title("⚙️ Settings")


model = st.sidebar.selectbox(
    "Choose Model",
    [
        "openai/gpt-oss-120b"
    ]
)


temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)


max_tokens = st.sidebar.slider(
    "Max Response Length",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)


# -----------------------------
# System Prompt
# -----------------------------

system_prompt = """
You are a Python tutor.
Answer questions clearly and simply.
Use examples when helpful.
Do not use bullet points unless necessary.
"""


# -----------------------------
# Initialize Chat History
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


# -----------------------------
# Clear Chat
# -----------------------------

if st.sidebar.button("Clear Chat"):

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    st.rerun()


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.messages:

    if message["role"] != "system":

        with st.chat_message(message["role"]):
            st.write(message["content"])


# -----------------------------
# Get User Message
# -----------------------------

user_message = st.chat_input(
    "Ask me anything..."
)


if user_message:

    # -----------------------------
    # Save User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # -----------------------------
    # Display User Message
    # -----------------------------

    with st.chat_message("user"):
        st.write(user_message)


    # -----------------------------
    # Send Message to FastAPI
    # -----------------------------

    with st.chat_message("assistant"):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": user_message
                }
            )


            # Check HTTP error
            response.raise_for_status()


            # Convert JSON response
            data = response.json()


            # Get AI response
            assistant_message = data["response"]


            # Display AI response
            st.write(assistant_message)


            # -----------------------------
            # Save AI Response
            # -----------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message
                }
            )


        except Exception as e:

            st.error(
                f"Error: {e}"
            )