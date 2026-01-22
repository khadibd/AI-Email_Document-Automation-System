#test_email_login.py

import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

print("Key loaded:", OPENAI_API_KEY is not None)
