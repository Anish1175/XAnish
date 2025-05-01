import os
from groq import Groq

# Correct way to get the env var
api_key = os.getenv("GROQ_API_KEY")

# Debug: print this temporarily to ensure it’s set (remove after testing)
if not api_key:
    raise ValueError("GROQ_API_KEY is not set!")

client = Groq(api_key=api_key)
