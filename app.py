import streamlit as st
import requests


# -----------------------------
# App Title
# -----------------------------

st.title("My AI Chatbot 🤖")


# -----------------------------
# Sidebar Settings
# -----------------------------

st.sidebar.title("⚙️ Settings")


model = st.sidebar.selectbox(
    "Choose Model",
    [
        "llama3.2:3b"
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
# Generate AI Response
# -----------------------------

    with st.chat_message("assistant"):

        try:

            # -----------------------------
            # Send Request to FastAPI
            # -----------------------------

            response = requests.post(
                "http://127.0.0.1:8003/chat",
                json={
                    "messages": st.session_state.messages,
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                stream=True
            )


            # -----------------------------
            # Check HTTP Error
            # -----------------------------

            response.raise_for_status()


            # -----------------------------
            # Empty Assistant Response
            # -----------------------------

            assistant_message = ""


            # -----------------------------
            # Create Placeholder
            # -----------------------------

            placeholder = st.empty()


            # -----------------------------
            # Receive Streaming Chunks
            # -----------------------------

            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True
            ):

                if chunk:

                    assistant_message += chunk

                    placeholder.markdown(
                        assistant_message
                    )


            # -----------------------------
            # Save AI Response
            # -----------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message
                }
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running on port 8002."
            )


        except requests.exceptions.HTTPError as e:

            st.error(
                f"FastAPI Error: {e}"
            )


        except Exception as e:

            st.error(
                f"Error: {e}"
            )
