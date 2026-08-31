import streamlit as st

st.title("My Chatbot 🤖")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_message = st.chat_input("Type your message...")

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # User message display
    with st.chat_message("user"):
        st.write(user_message)

    # Temporary AI response
    assistant_message = "I received your message 😊"

    # AI response save
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    # AI response display
    with st.chat_message("assistant"):
        st.write(assistant_message)