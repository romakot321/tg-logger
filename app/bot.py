import threading
import os
import telebot
import json
from message import Message, MessageRepository


def escape_markdown(text) -> str:
    special_chars = [
        '_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
    ]
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


class BotHandler:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "123")

    def __init__(self, message_repository: MessageRepository):
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.thread = threading.Thread(target=self.bot.infinity_polling)
        self.message_repository = message_repository

    def start(self):
        self._register()
        self.thread.start()

    def stop(self):
        self.bot.stop_bot()

    def send_message(self, msg: Message):
        text = f"Ошибка в контейнере {msg.container_name} в {msg.created_at}.\n```{msg.logs[:3900]}```"
        text = escape_markdown(text)
        for admin in self._list_admins():
            self.bot.send_message(admin, text, parse_mode="MarkdownV2")

    def _register(self):
        self.bot.register_message_handler(self._handle_add_admin_message, commands=['start'])

    def _handle_add_admin_message(self, message):
        print("Message from", message.from_user.id, message.chat.id, ":", message.text)
        token = message.text.split()
        if self.ACCESS_TOKEN not in token:
            return
        if self._add_admin(message.chat.id):
            self.bot.send_message(message.chat.id, "Вы подписались на уведомления об ошибках")

    def _add_admin(self, telegram_id: int):
        admins = self._list_admins()
        if telegram_id in admins:
            return False
        admins.append(telegram_id)
        with open('data/admins.json', 'w') as f:
            json.dump({"admins": admins}, f)
        return True

    def _list_admins(self) -> list[int]:
        try:
            with open('data/admins.json', 'r') as f:
                return json.load(f)["admins"]
        except FileNotFoundError:
            return []
