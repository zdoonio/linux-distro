#!/usr/bin/env python3
"""
AI Assistant z GUI (Tkinter) – komunikacja z LM Studio (lokalne API).
Umieść ten plik w: config/includes.chroot/usr/local/bin/ai_assistant.py
i nadaj mu prawo wykonywania (chmod +x).
"""

import tkinter as tk
import threading
import requests
import json
from dataclasses import dataclass, field

# ================== USTAWIENIA ==================
LM_STUDIO_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"
# =================================================

@dataclass
class Agent:
    model: str = "qwen3.5"
    base_url: str = LM_STUDIO_URL
    api_key: str = API_KEY
    messages: list[dict[str, str]] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 22500

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")

    def chat(self, user_message: str) -> str:
        """Wyślij wiadomość do API i zwróć odpowiedź asystenta."""
        self.messages.append({"role": "user", "content": user_message})
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        r = requests.post(url, headers=headers, json=payload, timeout=300)
        r.raise_for_status()
        data = r.json()
        choices = data.get("choices")
        if not choices:
            raise RuntimeError("Brak 'choices' w odpowiedzi API")
        message = choices[0].get("message")
        if not message:
            raise RuntimeError("Brak 'message' w odpowiedzi API")
        content = message.get("content")
        if not content:
            raise RuntimeError("Brak 'content' w wiadomości")
        self.messages.append(message)
        return content


class Application(tk.Tk):
    def __init__(self, agent: Agent):
        super().__init__()
        self.agent = agent
        self.title("AI Assistant – LM Studio")
        self.geometry("600x500")

        # Główne pole czatu
        self.chat_text = tk.Text(self, state="disabled", wrap="word")
        self.chat_text.pack(expand=True, fill="both", padx=5, pady=5)

        # Pasek przewijania
        scrollbar = tk.Scrollbar(self.chat_text)
        scrollbar.pack(side="right", fill="y")
        self.chat_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.chat_text.yview)

        # Ramka na pole wpisywania i przycisk
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=5, pady=5)

        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side="left", expand=True, fill="x")
        self.entry.bind("<Return>", self.send)

        self.send_btn = tk.Button(bottom_frame, text="Wyślij", command=self.send)
        self.send_btn.pack(side="right", padx=(5, 0))

        # Etykieta stanu (np. „Myślę…”)
        self.status = tk.Label(self, text="Gotowy", anchor="w")
        self.status.pack(fill="x", padx=5, pady=(0, 5))

        # Wątek odpowiedzi
        self._response_thread = None

    def log(self, message: str) -> None:
        """Dopisz wiadomość do okna czatu."""
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", message + "\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")

    def send(self, event=None) -> None:
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, "end")
        self.log(f"Ty: {user_input}")
        self.status.config(text="Myślę...")
        self.entry.config(state="disabled")
        self.send_btn.config(state="disabled")

        # Uruchom zapytanie w osobnym wątku, aby nie blokować GUI
        self._response_thread = threading.Thread(
            target=self._fetch_response, args=(user_input,), daemon=True
        )
        self._response_thread.start()

    def _fetch_response(self, user_message: str) -> None:
        try:
            answer = self.agent.chat(user_message)
            # Zaktualizuj GUI z głównego wątku
            self.after(0, self._on_response, answer)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_response(self, reply: str) -> None:
        self.log(f"AI: {reply}")
        self._finish()

    def _on_error(self, error_msg: str) -> None:
        self.log(f"Błąd: {error_msg}")
        self._finish()

    def _finish(self) -> None:
        self.status.config(text="Gotowy")
        self.entry.config(state="normal")
        self.send_btn.config(state="normal")
        self.entry.focus_set()


def main() -> None:
    agent = Agent(model="qwen3.5")  # zmień nazwę modelu, jeśli potrzebujesz
    app = Application(agent)
    app.mainloop()


if __name__ == "__main__":
    main()