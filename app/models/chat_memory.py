# app/utils/chat_memory.py

from typing import List, Dict
from collections import defaultdict

class ChatMemory:
    def __init__(self):
        self.memory = defaultdict(list)

    def add(self, session_id: str, role: str, content: str):
        self.memory[session_id].append({"role": role, "content": content})

    def get(self, session_id: str) -> List[Dict[str, str]]:
        return self.memory.get(session_id, [])

    def clear(self, session_id: str):
        self.memory.pop(session_id, None)
