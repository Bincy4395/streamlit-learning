
import streamlit as st
import requests


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# App Title
# ============================================================

st.title("My AI Chatbot 🤖")

st.caption(
    "Powered by FastAPI + Ollama + llama3.2:3b"
)


# ============================================================
# System Prompt
# ============================================================

system_prompt = """
You are a Python tutor.
Answer questions clearly and simply.
Use examples when helpful.
Do not use bullet points unless necessary.
"""


# ============================================================
# Initialize Chat History
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("⚙️ Settings")


# -----------------------------
# New Chat
# -----------------------------

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    st.rerun()


# -----------------------------
# Model
# -----------------------------

model = st.sidebar.selectbox(
    "Choose Model",
    [
        "llama3.2:3b"
    ]
)


# -----------------------------
# Temperature
# -----------------------------

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)


# -----------------------------
# Max Response Length
# -----------------------------

max_tokens = st.sidebar.slider(
    "Max Response Length",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)


# -----------------------------
# Model Information
# -----------------------------

st.sidebar.divider()

st.sidebar.markdown(
    "**🤖 Current Model**"
)

st.sidebar.info(
    f"{model}\n\n"
    "Running locally with Ollama"
)


# ============================================================
# Display Previous Messages
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# Chat Input
# ============================================================

user_message = st.chat_input(
    "Ask me anything about Python..."
)


if user_message:

    # ========================================================
    # Save User Message
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # ========================================================
    # Display User Message
    # ========================================================

    with st.chat_message("user"):

        st.markdown(user_message)


    # ========================================================
    # Generate AI Response
    # ========================================================

    with st.chat_message("assistant"):

        try:

            # ------------------------------------------------
            # Send Request to FastAPI
            # ------------------------------------------------

            response = requests.post(
                "http://127.0.0.1:8003/chat",

                json={
                    "messages": st.session_state.messages,
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },

                stream=True,

                timeout=120
            )


            # ------------------------------------------------
            # Check HTTP Error
            # ------------------------------------------------

            response.raise_for_status()


            # ------------------------------------------------
            # Prepare Streaming Response
            # ------------------------------------------------

            assistant_message = ""

            placeholder = st.empty()


            # ------------------------------------------------
            # Receive Streaming Chunks
            # ------------------------------------------------

            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True
            ):

                if chunk:

                    assistant_message += chunk

                    placeholder.markdown(
                        assistant_message + "▌"
                    )


            # ------------------------------------------------
            # Display Final Response
            # ------------------------------------------------

            placeholder.markdown(
                assistant_message
            )


            # ------------------------------------------------
            # Save AI Response
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message
                }
            )


        # ====================================================
        # Connection Error
        # ====================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI.\n\n"
                "Make sure the backend is running on port 8003."
            )


        # ====================================================
        # Timeout Error
        # ====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Request timed out.\n\n"
                "The AI model took too long to respond."
            )


        # ====================================================
        # HTTP Error
        # ====================================================

        except requests.exceptions.HTTPError as e:

            st.error(
                f"❌ FastAPI Error: {e}"
            )


        # ====================================================
        # General Error
        # ====================================================

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )
