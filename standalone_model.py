import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv('keys.env', override=True)

model = init_chat_model(
    model='mistral-medium-2508',
    temperature=0.1
)

response = model.invoke('Hello, what is python?')

print(response)
print(response.content)

