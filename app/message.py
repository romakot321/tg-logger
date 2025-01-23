from dataclasses import dataclass
import datetime as dt


@dataclass
class Message:
    container_name: str
    logs: str
    created_at: dt.datetime


class MessageRepository:
    def __init__(self):
        self._messages = []

    def add(self, container_name: str, logs: str):
        self._messages.append(
            Message(container_name=container_name, logs=logs, created_at=dt.datetime.now())
        )

    def list(self) -> list[Message]:
        return self._messages.copy()

    def clear(self):
        self._messages.clear()

