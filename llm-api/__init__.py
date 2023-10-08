from dotenv import load_dotenv
from os import getenv
import openai

load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")