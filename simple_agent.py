import requests
import os
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


load_dotenv('keys.env', override=True)

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city"""
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    data = response.json()
    return f"The weather in {city} is {data['current_condition'][0]['weatherDesc'][0]['value']}"

model = ChatOpenAI(model='gpt-4o-mini')  

agent = create_react_agent(
    model=model,
    tools=[get_weather],
    prompt
    ='You are a helpful assistant that can provide weather information for any city who always cracks jokes and is humorous while remaining helpful.'
)

response = agent.invoke({
    'messages': [{          # ✅ 'messages' not 'message'
        'role': 'user',
        'content': 'What is the weather in New York?'
    }]
})

print(response)
print(response['messages'][-1].content)  # ✅ 'messages' not 'message'