from watcher import Watcher
from message import Message, MessageRepository
from bot import BotHandler
import os
import docker


def get_container_names() -> list[str]:
    if os.getenv("CONTAINER_NAMES") is None:
        return []
    return os.getenv("CONTAINER_NAMES").split(',')


def watch_for_messages(sender: BotHandler, msg_rep: MessageRepository):
    while True:
        messages = msg_rep.list()
        if not messages:
            continue
        print(messages)

        for msg in messages:
            sender.send_message(msg)
        msg_rep.clear()


def main():
    msg_rep = MessageRepository()
    poller = BotHandler(msg_rep)
    sender = BotHandler(msg_rep)
    docker_client = docker.from_env()
    watchers = []

    for container_name in get_container_names():
        watchers.append(Watcher(container_name, docker_client, msg_rep))
    if not watchers:
        print("WARNING: You not specified any container in CONTAINER_NAMES env")

    poller.start()
    [w.start() for w in watchers]
    try:
        watch_for_messages(sender, msg_rep)
    except KeyboardInterrupt:
        print("Trying to stop...")
        poller.stop()
        [w.stop() for w in watchers]


if __name__ == "__main__":
    assert BotHandler.BOT_TOKEN is not None, "Specify BOT_TOKEN env"
    main()
