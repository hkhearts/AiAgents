from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import cohere

# Step 1: Load and caption the image using BLIP
print("⏳ Loading BLIP model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Replace 'your_image.png' with your image file path
image_path = "fic.jpg"
image = Image.open(image_path).convert("RGB")

# Generate caption
inputs = processor(images=image, return_tensors="pt")
out = model.generate(**inputs)
image_caption = processor.decode(out[0], skip_special_tokens=True)

print("🖼️ Image Caption:", image_caption)

# Step 2: Use Cohere to generate a fictional story
co = cohere.Client("BfjTIcPZteAiqRQE3tM1NaELjiUB2QDHRtYrAFDe")  # Replace with your actual Cohere API key

prompt = f"Write a 3-sentence fictional story based on this image description: {image_caption}"

response = co.chat(
    model="command-r-plus",
    message=prompt
)

print("\n📖 Fictional Story:\n")
print(response.text.strip())
