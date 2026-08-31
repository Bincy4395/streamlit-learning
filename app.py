import streamlit as st
from huggingface_hub import InferenceClient


# -----------------------------
# Hugging Face setup
# -----------------------------

token = st.secrets["HF_TOKEN"]

client = InferenceClient(
    api_key=token
)


# -----------------------------
# App title
# -----------------------------

st.title("My AI Chatbot 🤖")


# -----------------------------
# System prompt
# -----------------------------

system_prompt = """
You are a Python tutor.
Answer questions clearly and simply.
Use examples when helpful.
Do not use bullet points unless necessary.
"""


# -----------------------------
# Sidebar Settings
# -----------------------------

st.sidebar.title("⚙️ Settings")


# Model selection
model = st.sidebar.selectbox(
    "Choose Model",
    [
        "openai/gpt-oss-120b"
    ]
)


# Temperature
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)


# Maximum response length
max_tokens = st.sidebar.slider(
    "Max Response Length",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)


# -----------------------------
# Initialize chat history
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
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    # Don't display system prompt
    if message["role"] != "system":

        with st.chat_message(message["role"]):
            st.write(message["content"])


# -----------------------------
# Get user message
# -----------------------------

user_message = st.chat_input(
    "Ask me anything..."
)


if user_message:

    # -----------------------------
    # Save user message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # -----------------------------
    # Display user message
    # -----------------------------

    with st.chat_message("user"):
        st.write(user_message)


    # -----------------------------
    # Generate AI response
    # -----------------------------

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )


            # Empty response initially
            assistant_message = ""


            # Placeholder for streaming
            placeholder = st.empty()


            # Receive chunks
            for chunk in response:

                content = chunk.choices[0].delta.content

                if content:

                    assistant_message += content

                    placeholder.markdown(
                        assistant_message
                    )


            # -----------------------------
            # Save AI response
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