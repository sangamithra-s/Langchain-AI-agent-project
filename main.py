from langchain_core.tools import tool
from langchain.tools import ToolRuntime     #to save context and use it in the tools

print(hasattr(langchain.tools, "ToolRuntime"))