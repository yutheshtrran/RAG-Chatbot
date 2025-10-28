import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-09-2025",
    contents=["Hello! Can you explain dengue fever treatment?"]
)

print(response.text)
