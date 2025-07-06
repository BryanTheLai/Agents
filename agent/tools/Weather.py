import json

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    return json.dumps({"location": location, "temperature": "30", "unit": unit})

get_current_weather_params = {
    "type": "object",
    "properties": {
        "location": {"type": "string", "description": "The city and state, e.g. 'San Francisco, CA'"},
        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "fahrenheit", "description": "Temperature unit ('celsius' or 'fahrenheit')"},
    },
    "required": ["location"],
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": get_current_weather_params,
        },
    }
]