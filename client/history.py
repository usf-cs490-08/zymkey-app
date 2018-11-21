from threading import Lock
from copy import deepcopy

class Message:
    def __init__(self, message, timestamp):
        self.message = message
        self.timestamp = timestamp

class History:

    def __init__(self):
        self.history = {}
        self.lock = Lock()

    def putMessage(self, userList, message, timestamp):
        message = Message(message, timestamp)
        name = ','.join(userList)
        self.lock.acquire()
        if name not in self.history:
            self.history[name] = []
        self.history[name].append(message)
        self.lock.release()

    def getConversation(self, userList):
        copy = None
        userList.sort()
        name = ','.join(userList)
        self.lock.acquire()
        if self.history[name]:
            copy = deepcopy(self.history[name])
        self.lock.release()
        return copy

    def listConversations(self):
        convs = []
        self.lock.acquire()
        for k, v in self.history.items():
            convs.append(k)
        self.lock.release()
        return convs