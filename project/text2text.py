import streamlit as st
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Function to get response from Cohere
def get_cohere_response(question):
    response = co.chat(
        model='command',
        message=question,
        max_tokens=100,
        temperature=0.5
    )
    return response.text

# Streamlit app setup
st.set_page_config(page_title="HerSeek", page_icon="🤖")
st.title("HerSeek Chat Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = get_cohere_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})