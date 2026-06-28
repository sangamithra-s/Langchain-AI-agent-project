import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

load_dotenv('keys.env', override=True)

model = init_chat_model(
    model='mistral-medium-2508',
    temperature=0.1
)

# conversation = [
#     SystemMessage(content="You are a helpful assistant for questions regarding programming"),
#     HumanMessage(content="Hello, what is python?"),
#     AIMessage(content="Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. Python is widely used for web development, data analysis, artificial intelligence, scientific computing, and more.")
#     ,HumanMessage(content="What is the difference between python and java?")
# ]

# response = model.invoke(conversation)

#Streaming response
for chunk in model.stream('Hello, what is python?'):
    print(chunk.text, end='', flush=True)


# print(response)
# print(response.content)

