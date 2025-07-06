from litellm import completion
from dotenv import load_dotenv
from agent.tools.Weather import tools, get_current_weather
from agent.tools.utils import handle_tool_calls
import json

def detect_response_type(msg, history_msg, available_functions):
    # Append a dict representation of the message for JSON serialization
    history_msg.append({
        "role": msg.role,
        "content": msg.content,
        "tool_calls": getattr(msg, "tool_calls", None)
    })
    # Function call request
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        handle_tool_calls(msg.tool_calls, history_msg, available_functions)
        return "function_call"#, msg.tool_calls
    # Attempt structured JSON
    if msg.content:
        try:
            #parsed = json.loads(msg.content)
            return "structured_json"#, parsed
        except (json.JSONDecodeError, TypeError):
            return "plain_text"#, msg.content
    return "unknown"#, None

load_dotenv()

history_messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris in celsius?"}]
model="gemini/gemini-2.5-flash-lite-preview-06-17"
available_functions = {"get_current_weather": get_current_weather}

first_response = completion(
  model=model,
  messages=history_messages, 
  tools=tools,
  tool_choice="auto",
  )

first_msg = first_response.choices[0].message
first_response_type = detect_response_type(first_msg, history_messages, available_functions)

second_response = completion(
    model=model,
    messages=history_messages,
)

second_msg = second_response.choices[0].message
second_resp_type = detect_response_type(second_msg, history_messages, available_functions)
print(f"Detected: {second_resp_type}")
print(second_msg.content)

print(json.dumps(history_messages, indent=2, default=str))