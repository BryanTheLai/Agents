import json
from typing import Any, Callable, Dict, List

def handle_tool_calls(
    tool_calls: List[Any],
    messages: List[Dict[str, Any]],
    available_functions: Dict[str, Callable[..., str]],
) -> None:
    """
    Execute LLM tool calls, append results to messages.
    """
    
    for call in tool_calls:
        # if toolcall not in available_functions, then the result should be error, tool not found.
        
        print(f"\nExecuting tool call\n{call}")
        if call.function.name in available_functions:
            fn = available_functions.get(call.function.name)
            kwargs = json.loads(call.function.arguments)
            result = fn(**kwargs)
            print(f"Result from tool call\n{result}\n")
            messages.append({
                "tool_call_id": call.id,
                "role": "tool",
                "name": call.function.name,
                "content": result,
            })
        else:
            messages.append({
                "tool_call_id": call.id,
                "role": "tool",
                "name": call.function.name,
                "content": "Error: Function/Tool not found in available_functions",
            })
        
