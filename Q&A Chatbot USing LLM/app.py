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
        model='command',  # Use 'command' or another available chat model
        message=question,
        max_tokens=100,
        temperature=0.5
    )
    return response.text

# Streamlit app setup
st.set_page_config(page_title="Q&A Demo")
st.header("Cohere Q&A Bot")

input_question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input_question:
    st.subheader("The Response is")
    st.write(get_cohere_response(input_question))