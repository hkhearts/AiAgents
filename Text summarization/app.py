# import cohere

# # Replace with your actual Cohere API key
# cohere_api_key = 'BfjTIcPZteAiqRQE3tM1NaELjiUB2QDHRtYrAFDe'

# # Initialize Cohere client
# co = cohere.Client(cohere_api_key)

# # Your input text
# text = """
# OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence benefits all of humanity. We are governed by a nonprofit and unique capped-profit model that drives our commitment to safety and broad benefit.
# """

# # Generate a summary
# response = co.summarize(
#     text=text,
#     length='medium',         # Options: 'short', 'medium', 'long', 'auto'
#     format='paragraph',      # Options: 'paragraph', 'bullets'
#     model='summarize-xlarge',# Best available summarization model
#     temperature=0.3          # Controls creativity
# )

# # Print the summary
# print("Summary:\n", response.summary)

import streamlit as st
import cohere

# Set your Cohere API key
COHERE_API_KEY = 'BfjTIcPZteAiqRQE3tM1NaELjiUB2QDHRtYrAFDe'  # Replace with your actual API key

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Streamlit App UI
st.title("Text Summarization with Cohere")
st.write("Enter a paragraph below to get a summary using Cohere's API.")

# Text input from user
user_input = st.text_area("Input Paragraph", height=200)

# Options for summary configuration
length = st.selectbox("Summary Length", ["short", "medium", "long", "auto"])
format_option = st.selectbox("Summary Format", ["paragraph", "bullets"])
temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.3)

# Button to generate summary
if st.button("Summarize") and user_input.strip():
    with st.spinner("Summarizing..."):
        try:
            response = co.summarize(
                text=user_input,
                length=length,
                format=format_option,
                model='summarize-xlarge',
                temperature=temperature
            )
            st.subheader("Summary")
            st.success(response.summary)
        except Exception as e:
            st.error(f"Error: {e}")

