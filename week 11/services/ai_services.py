# services/ai_assistant.py

from typing import List, Dict


class AIAssistant:
    # simple wrapper around an ai/chat model.

    def __init__(self, system_prompt: str = "you are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []  # history is kept private

    def set_system_prompt(self, prompt: str):
        # changes the system prompt
        self._system_prompt = prompt

    def send_message(self, user_message: str):
        # sends a message and gets a response (replace this with your real api call)

        # append user message to history
        self._history.append({"role": "user", "content": user_message})

        # fake response for now:
        response = f"ai reply to: {user_message[:50]}"

        # append ai response to history
        self._history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        # clears the chat history
        self._history.clear()