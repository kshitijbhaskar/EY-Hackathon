import streamlit as st
import time

# Predefined messages and responses
messages_and_responses = [
    {"role": "assistant", "content": "Hello there! How can I assist you today?"},
    {"role": "user", "content": "What's the weather like?"},
    {"role": "assistant", "content": "I'm sorry, I can't provide real-time data."},
    # Add more predefined messages and responses here
]

st.title("Automated chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# If the chat history is empty, wait for a few seconds and then send the first message
if not st.session_state.messages:
    time.sleep(3)  # Wait for 3 seconds
    first_message = {"role": "user", "content": "Hello, bot!"}
    st.session_state.messages.append(first_message)
    with st.chat_message(first_message["role"]):
        st.markdown(first_message["content"])
# Loop through predefined messages and responses
for message in messages_and_responses:
    # Add message to chat history
    st.session_state.messages.append(message)
    # Display message in chat message container
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    # Wait for a while before displaying the next message
    time.sleep(3)

