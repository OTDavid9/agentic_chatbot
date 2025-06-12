# Setup OpenAI API Client
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file         

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")



client = OpenAI(
    base_url= OLLAMA_BASE_URL,
    api_key= OPENAI_API_KEY,  # Still required, even if ignored by backend
)