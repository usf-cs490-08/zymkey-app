from threading import Lock
from copy import deepcopy

class Status:
    def __init__(self, isOnline, timestamp):
        self.isOnline = isOnline
        self.timestamp = timestamp

class StatusMap:

    def __init__(self):
        self.users = {}
        self.lock = Lock()

    def putStatus(self, user, isOnline, timestamp):
        status = Status(isOnline, timestamp)
        self.lock.acquire()
        self.users[user] = status
        self.lock.release()

    def all(self):
        copy = None
        self.lock.acquire()
        copy = deepcopy(self.users)
        self.lock.release()
        return copy