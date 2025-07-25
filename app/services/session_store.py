import uuid
import os

RESP_DIR = "responses"
os.makedirs(RESP_DIR, exist_ok=True)

def save_response(content: str) -> str:
    session_id = str(uuid.uuid4())
    file_path = os.path.join(RESP_DIR, f"{session_id}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return session_id

def load_response(session_id: str) -> str:
    file_path = os.path.join(RESP_DIR, f"{session_id}.html")
    if not os.path.exists(file_path):
        return "<p>Session not found.</p>"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
