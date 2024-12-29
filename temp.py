import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise ValueError("API key for Gemini is missing. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")


prompt = "What are the most important skills for a data scientist?"

responce = model.generate_content(prompt)
print(responce.text.strip())

