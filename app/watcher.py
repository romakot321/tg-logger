import time
import threading
from message import MessageRepository
import docker


class Watcher:
    UPDATE_TIME = 30
    LOGS_SINCE = 31

    def __init__(
            self,
            container_name,
            docker_client,
            message_repository: MessageRepository
    ):
        self.thread = threading.Thread(target=self._watch)
        self.docker_client = docker_client
        self.container_name = container_name
        self.message_repository = message_repository
        self.running = True
        self.container = docker_client.containers.get(container_name)

    def _watch(self):
        while self.running:
            time.sleep(self.UPDATE_TIME)
            try:
                logs = self.container.logs(since=int(time.time()) - self.LOGS_SINCE).decode('utf-8')
            except docker.errors.NotFound:
                self.container = self.docker_client.containers.get(self.container_name)
                logs = self.container.logs(since=int(time.time()) - self.LOGS_SINCE).decode('utf-8')

            if 'error' in logs.lower():
                print("Error in", self.container_name)
                self.message_repository.add(self.container_name, logs)

    def stop(self):
        self.running = False

    def start(self):
        self.thread.start()

