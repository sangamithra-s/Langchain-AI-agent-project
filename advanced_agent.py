from dataclasses import dataclass
import requests
import os
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langchain.tools import ToolRuntime

from langgraph.checkpoint.memory import InMemorySaver

load_dotenv('keys.env', override=True)

@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city"""
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    data = response.json()
    return f"The weather in {city} is {data['current_condition'][0]['weatherDesc'][0]['value']}"


@tool('locate_user', description="Get the location of the user based on the context")
def locate_user(runtime: ToolRuntime[Context]):
    user_id = runtime.context.user_id
    if user_id == 'ABC123':
        return 'New York'
    elif user_id == 'XYZ456':
        return 'Los Angeles'
    elif user_id == 'HLJ989':
        return 'Paris'
    else:
        return 'Unknown location'


model = ChatMistralAI(model='mistral-medium-2508', temperature=0.3)
checkpoint_saver = InMemorySaver()

# ✅ Removed response_format here — it breaks with Mistral
agent = create_react_agent(
    model=model,
    tools=[get_weather, locate_user],
    prompt='You are a helpful assistant that can provide weather information for any city who always cracks jokes and is humorous while remaining helpful.',
    context_schema=Context,
    checkpointer=checkpoint_saver
)

config = {'configurable': {'thread_id': '2'}}  # ✅ thread_id as string, fixes the Pydantic warning

response = agent.invoke(
    {
        'messages': [{
            'role': 'user',
            'content': 'yes you are right'
        }]
    },
    config=config,
    context=Context(user_id='HLJ989')
)

final_message = response['messages'][-1].content
print("Agent response:", final_message)



# ✅ Structured output done separately, AFTER the agent finishes
structured_model = model.with_structured_output(ResponseFormat)
structured_response = structured_model.invoke(
    f"Extract structured weather data from this text: {final_message}"
)

print("------")

print(structured_response['summary'])
print(structured_response['temperature_celsius'])
print(structured_response['temperature_fahrenheit'])
print(structured_response['humidity'])