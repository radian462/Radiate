import fireworks.client
import os
import re
import google.generativeai as genai
import requests

TOKEN = os.getenv("fireworks_api")

fireworks.client.api_key = TOKEN

def chatllama(text):
  completion = fireworks.client.ChatCompletion.create(
    model="accounts/fireworks/models/elyza-japanese-llama-2-7b-fast-instruct",
    messages=[
        {
            "role": "user",
            "content": text,
        }
    ],
    stream=False,
    n=1,
    max_tokens=150,
    temperature=0.1,
    top_p=0.9,
)
  return(completion.choices[0].message.content)

def chatgemini(text):
  genai.configure(api_key=os.getenv("gemini_api_key"))

  model = genai.GenerativeModel('gemini-pro')

  text = re.sub(' gemini', '', text)
  text = re.sub(' bard', '', text)

  response = model.generate_content(text,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=145,
        temperature=0.1))

  return(response.text)

def chatgpt(text):
  url = "https://api-mebo.dev/api"
  headers = {'content-type': 'application/json'}
  item_data = {
    "api_key": os.getenv('miibo_API'),
    "agent_id": os.getenv('miibo_ID'),
    "utterance": text,
  }

  r = requests.post(url,json=item_data,headers=headers)

  return r.json()["bestResponse"]["utterance"]