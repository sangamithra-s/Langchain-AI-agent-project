import os
import requests
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv('keys.env', override=True)

print("KEY:", os.environ.get("OPENAI_API_KEY")) 