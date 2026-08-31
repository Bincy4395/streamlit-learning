import streamlit as st

st.title("My Chatbot 🤖")

# Chat history initialize ചെയ്യുന്നു
if "messages" not in st.session_state:
    st.session_state.messages = []

# പഴയ messages display ചെയ്യുന്നു
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# പുതിയ message എടുക്കുന്നു
user_message = st.chat_input("Type your message...")

if user_message:

    # User message save ചെയ്യുന്നു
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # User message display
    with st.chat_message("user"):
        st.write(user_message)

    # Temporary AI response
    assistant_message = "I received your message 😊"

    # AI response save ചെയ്യുന്നു
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    # AI response display
    with st.chat_message("assistant"):
        st.write(assistant_message)