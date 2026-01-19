# import Gemini API lib
from google import genai
# import content config
from google.genai.types import GenerateContentConfig
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# initializing OpenAI client via API Token
# export GEMINI_API_KEY=your_key actually using in prod env instead .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# creating response
# ======================
# client - client SDK object for Gemini API
# models - subsistem inside the client responsible for the work with Gemini models
# generate_content - generate text using model. Has arguments:
#   1. model - which model we chose to generate content
#   2. contents - messages and instructions for model
#   3. generation_configs - configs of temperature, length etc.
# ======================
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    # building instructions for model via GenerateContentConfig
    # making instruction for model as AI role in improvized roleplay
    config=GenerateContentConfig(
        # such as system role in OpenAI model
        system_instruction=[
            "You are a professional teacher. Explain simply."
        ],
        # model's imagination (0 ≤ temp ≤ 2)
        temperature=0.5,
        # max count of response's tokens (token == one word/punctuation mark)
        max_output_tokens=100,
        # variants limitation for answers (0 ≤ top_p ≤ 1)
        top_p=0.9,
    ),
    contents=[
        # there's one interesting thing:
        # in gemini we can use system_instructions (preferable) OR
        # making these instructions in first message (not preferable)
        # both you can use such as system role in OpenAI

        # {
        #     "role": "user",
        #     "parts": [
        #         {"text": "You are a professional teacher. Explain simply."}
        #     ]
        # },
        {
            # there are 2 roles in gemini
            #   1. user - your question to model
            #   2. model - model's answer to your question
            "role": "user",
            # you can divide your content to parts
            "parts": [
                {"text": "What is an LLM?"}
            ]
        }
    ]
)

# printing model's response
# such as OpenAI, there's candidates for your response (we chose first),
# content from candidate,
# we chose first part of that content and printing text from it

# you can also use print(response.text)
# but if something goes wrong you wont get additional info, only None
print(response.candidates[0].content.parts[0].text)