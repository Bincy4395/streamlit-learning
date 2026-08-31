import streamlit as st
from huggingface_hub import InferenceClient

# Hugging Face token
token = st.secrets["HF_TOKEN"]

# Hugging Face client
client = InferenceClient(
    api_key=token
)

st.title("My AI Chatbot 🤖")

# Chat history initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get new user message
user_message = st.chat_input("Ask me anything...")

if user_message:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    # Send complete conversation to AI
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=st.session_state.messages
    )

    # Get AI response
    assistant_message = response.choices[0].message.content

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    # Display AI response
    with st.chat_message("assistant"):
        st.write(assistant_message)