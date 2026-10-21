import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3.8-27b"
BASE_URL = "https://api.groq.com/openai/v1"


TEMPERATURE = 0.1 
MAX_TOKENS = 1500