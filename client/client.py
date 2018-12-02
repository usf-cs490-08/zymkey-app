from history import History
from status import StatusMap
from sender import MessageSender
from receiver import MessageReceiver
from users import UserStatusManager
import re

class ChatClient:

    BROKER_LIST = 'mcvm155:9092'

    def __init__(self, user):
        self.user = user
        self.history = History()
        self.statusMap = StatusMap()
        self.sender = MessageSender(self.BROKER_LIST, user)
        self.receiver = MessageReceiver(self.BROKER_LIST, user, self.history)
        self.userManager = UserStatusManager(self.BROKER_LIST, user, self.statusMap)

        self.userManager.goOnline()

    def sendMessage(self, userList, message):
        self.sender.sendMessage(userList, message)

    def listConversations(self):
        filtered = []
        for conv in self.history.listConversations():
            users = re.split(',', conv)
            if self.user in users and len(users) > 1:
                users.remove(self.user)
            filtered.append(','.join(users))
        return filtered

    def getConversation(self, userList):
        if 'GLOBAL' not in userList:
            if self.user not in userList:
                userList.append(self.user)
        return self.history.getConversation(userList)

    def getUsers(self):
        return self.statusMap.all()
    
    def shutdown(self):
        self.userManager.goOffline()
        self.receiver.shutdown()