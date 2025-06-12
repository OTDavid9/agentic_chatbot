from openai import OpenAI
import requests
import json
from chat_application.tools import ollama_tools
from chat_application.functions import *
from chat_application.system_prompt import system_prompt
from chat_application.tool_registry import TOOL_REGISTRY
import logging
from openai_client.client import client
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
FASTAPI_URL = os.getenv("FASTAPI_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

# HTTP session for API requests
session = requests.Session()

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": system_prompt},
]

def process_tool_calls(tool_calls):
    """Process tool calls and return results using dynamic dispatch."""
    tool_responses = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        logging.info(f"🛠️  Tool called: {tool_name} with args: {args}")

        # Get the function from the dispatcher
        func = TOOL_REGISTRY.get(tool_name)

        if func:
            try:
                result = func(**args)
            except Exception as e:
                result = f"Error while executing {tool_name}: {str(e)}"
        else:
            result = f"Error: Unknown tool {tool_name}"

        tool_responses.append({
            "role": "tool",
            "name": tool_name,
            "content": str(result),
            "tool_call_id": tool_call.id
        })

    return tool_responses


def chat_loop():
    """Main chat loop for continuous conversation."""
    global conversation_history

    print("Starting conversation. Type 'quit' to exit.")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        user_input = user_input + " " + "/no_think"

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        # Continue conversation until no more tool calls are needed
        while True:
            # Prepare messages: system prompt + last 10 items
            truncated_converstaion = [conversation_history[0]] + conversation_history[-10:]

            # Get model response
            response = client.chat.completions.create(
                messages=truncated_converstaion,
                model=MODEL_NAME,
                tools=ollama_tools,
                tool_choice="auto",
                temperature=0.9
            )

            message = response.choices[0].message
            response = response.choices[0].message.content
            response = response.strip()

            clean_response = response.replace("<think>\n\n</think>", "").strip()

            # Add assistant response to full history
            conversation_history.append({
                "role": "assistant",
                "content": clean_response,
                "tool_calls": message.tool_calls if hasattr(message, 'tool_calls') else None
            })

            # If there are tool calls, process them and continue
            if message.tool_calls:
                tool_responses = process_tool_calls(message.tool_calls)
                conversation_history.extend(tool_responses)
            else:
                # No more tool calls, display response and break
                if message.content:
                    print(f"Assistant: {clean_response}")
                break

if __name__ == "__main__":
    chat_loop()
