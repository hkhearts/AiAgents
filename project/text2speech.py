import streamlit as st
import cohere
import os
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO

# Load environment variables
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Function to enhance text using Cohere (optional)
def enhance_text(text):
    if not text.strip():
        return text
    try:
        response = co.generate(
            model='command',
            prompt=f"Improve this text while keeping its core meaning:\n{text}",
            max_tokens=100,
            temperature=0.5
        )
        return response.generations[0].text
    except Exception as e:
        st.error(f"Error enhancing text: {e}")
        return text

# Function to convert text to speech
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

# Streamlit app setup
st.set_page_config(page_title="Text to Speech Converter", page_icon="🔊")
st.title("Text to Speech Converter")

# Text input area
user_text = st.text_area("Enter your text here:", height=150)

# Options
col1, col2 = st.columns(2)
with col1:
    enhance = st.checkbox("Enhance text with AI", value=False)
with col2:
    voice_speed = st.slider("Speech speed", 0.5, 2.0, 1.0)

# Convert button
if st.button("Convert to Speech"):
    if user_text.strip():
        with st.spinner("Processing..."):
            # Enhance text if option is selected
            final_text = enhance_text(user_text) if enhance else user_text
            
            # Show the text that will be converted
            if enhance:
                st.subheader("Enhanced Text")
                st.write(final_text)
            
            # Convert to speech
            audio_bytes = text_to_speech(final_text)
            
            # Play the audio
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')
                
                # Download button
                st.download_button(
                    label="Download Audio",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("Please enter some text to convert")