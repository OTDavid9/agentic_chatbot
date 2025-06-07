import json
from openai import OpenAI
from tools import tools # type: ignore
from functions import make_purchase, order_items
from system_prompt import system_prompt
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")



client = OpenAI(
    api_key= OPENAI_API_KEY,
    base_url= OLLAMA_BASE_URL

)

user_input = input("User input:")


conversation = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input},

]

response = client.chat.completions.create(
    model="granite3.3:8b",
    messages=conversation,
    tools=tools,
    tool_choice='auto'
)
print(response)
print(f"AI response: {response.choices[0].message.content}")

if response.choices[0].message.tool_calls is not None:
    for tool_call in response.choices[0].message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        print(f"Tool name: {tool_name}")
        print(f"Tool arguments: {tool_args}")

        if tool_name == "make_purchase":
            result = make_purchase(**tool_args)
            print(result)
        elif tool_name == "order_items":
            result = order_items(**tool_args)
            print(result)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        
        








    