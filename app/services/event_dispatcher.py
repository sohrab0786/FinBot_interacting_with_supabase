# app/services/event_dispatcher.py
import uuid
def query_loading_event(task_names):
    return {"type": "query-loading", "content": {"isLoading": True, "taskNames": task_names}}

def tool_call_event(tool_name, args):
    return {"type": "toolCall", "content": {"toolCallId": str(uuid.uuid4()), "toolName": tool_name, "args": args}}

def tool_result_event(tool_call_id, result):
    return {"type": "toolResult", "content": {"toolCallId": tool_call_id, "result": result}}

def query_finished_event():
    return {"type": "query-loading", "content": {"isLoading": False, "taskNames": []}}
