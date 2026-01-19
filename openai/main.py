# import openai lib
from openai import OpenAI
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# initializing OpenAI client via API Token
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# creating response
# ======================
# client - initialized OpenAI client
# chat - dialogue mode
# completions - answer genetarion, ends/completes requests's text
# create - create request and send to OpenAI API
# ======================
response = client.chat.completions.create(
    model="gpt-4o-mini", # <- chose GPT model
    messages=[ # <- building messages
        # ======================
        # ROLE
        #   there are 3 roles in GPT model such as:
        #   1. System - instruction for model as AI role in improvized roleplay
        #   2. User - is your question to model
        #   3. Assistant - is the model's answer
        # ======================
        {"role": "system", "content": "You are a professional teacher. Explain simply."},
        {"role": "user", "content": "What is an LLM?"}
    ],
    # temperature is the coefficient of model's imagining, 0 ≤ temp ≤ 2
    # bigger value - greater imagining (and bigger mistakes :))
    temperature=0.7
)

# printing the response result
# from response using first choice, getting content from current choice message
print(response.choices[0].message.content)