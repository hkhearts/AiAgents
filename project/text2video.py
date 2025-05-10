import streamlit as st
import cohere
import openai
from moviepy.editor import ImageSequenceClip
from PIL import Image
import requests
import uuid
import os

# === Config ===
cohere_api_key = "YOUR_COHERE_API_KEY"
openai_api_key = "YOUR_OPENAI_API_KEY"
co = cohere.Client(cohere_api_key)
openai.api_key = openai_api_key

output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# === Streamlit UI ===
st.title("🎬 Script-to-Video Generator")
script = st.text_area("Enter your script (text-based scene description):", height=200)

if st.button("Generate Video"):
    if not script.strip():
        st.warning("Please enter a script.")
    else:
        with st.spinner("Generating scenes using Cohere..."):
            response = co.generate(
                model="command",
                prompt=f"Break the following script into distinct visual scenes:\n\n{script}",
                max_tokens=300,
                temperature=0.7
            )
            scenes = response.generations[0].text.strip().split("\n")
            scenes = [s for s in scenes if s.strip()]

        image_paths = []

        with st.spinner("Generating images and creating video..."):
            for idx, scene in enumerate(scenes):
                prompt = scene.strip()

                image_response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                image_url = image_response["data"][0]["url"]

                # Download and save the image
                img = Image.open(requests.get(image_url, stream=True).raw)
                filename = f"{uuid.uuid4()}.png"
                filepath = os.path.join(output_folder, filename)
                img.save(filepath)
                image_paths.append(filepath)

            # Create video
            clip = ImageSequenceClip(image_paths, fps=1)
            video_path = os.path.join(output_folder, "output_video.mp4")
            clip.write_videofile(video_path, audio=False)

        st.success("Video created successfully!")
        st.video(video_path)
