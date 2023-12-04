import fireworks.client
import os

TOKEN = os.getenv("fireworks_api")

fireworks.client.api_key = TOKEN

def chatfireworks(question):
  completion = fireworks.client.ChatCompletion.create(
    model="accounts/fireworks/models/elyza-japanese-llama-2-7b-fast-instruct",
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    stream=False,
    n=1,
    max_tokens=150,
    temperature=0.1,
    top_p=0.9,
)
  return(completion.choices[0].message.content)
