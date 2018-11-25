import re
from client import ChatClient
from history import Message

class Interface:

    USER_MAX_SIZE = 15
    HELP_STR = \
'''
  help                               - see this menu
  users                              - display all users and their status
  ls                                 - list all conversations
  open [-d] <NAME>[,...,<NAME>]      - display conversation ('-d' for dates)
  send <NAME>[,...,<NAME>] <MESSAGE> - send a message to user
  bcast <MESSAGE>                    - send a message to everyone
  exit                               - exit the program
'''
    HELP_CMD = 'help'
    USERS_CMD = 'users'
    LS_CMD = 'ls'
    OPEN_CMD = 'open'
    SEND_CMD = 'send'
    BCAST_CMD = 'bcast'
    EXIT_CMD = 'exit'
    CONV_DELIM = ','

    def __init__(self):
        self.user = Interface.getUserId()
        self.client = ChatClient(self.user)

    @staticmethod
    def getUserId():
        print()
        user = ''
        while user == '' or len(user) > Interface.USER_MAX_SIZE:
            user = input('user: ')
            user = re.sub('[\s+]', '', user)  # TODO replace all characters that are invalid in a topic name
            if len(user) > Interface.USER_MAX_SIZE:
                print('user must < %s characters' % Interface.USER_MAX_SIZE)
        print()
        return user

    def run(self):
        shutdown = False
        while not shutdown:

            # prompt
            print(self.user + ' > ', end='')
            line = input()

            if line == '':
                continue

            # parse into array (& allow use of quotes)
            cmd = [re.sub('["\']', '', c[0]) for c in re.findall('([^\'"]\\S*|([\'"]).+?\\2)\\s*', line)]

            def invalidCmd(c):
                print('error: invalid use of \'%s\'; see \'help\' menu' % c)

            if cmd[0] == self.HELP_CMD:
                # help
                print(self.HELP_STR)
            elif cmd[0] == self.USERS_CMD:
                # users
                print(self.client.getUsers())
            elif cmd[0] == self.LS_CMD:
                # ls
                print(self.client.listConversations())
            elif cmd[0] == self.OPEN_CMD:
                # open [-d] <NAME>[,...,<NAME>]
                if len(cmd) < 2:
                    invalidCmd(cmd[0])
                else:
                    showTime = False
                    userList = None
                    for arg in cmd[1:]:
                        if arg.lower() == '-d':
                            showTime = True
                        else:
                            userList = re.split(',', arg)
                    for mes in self.client.getConversation(userList):
                        if showTime:
                            # TODO print timestamp + message
                            pass
                        else:
                            # TODO add 'from' field
                            print(mes.message)
                pass
            elif cmd[0] == self.SEND_CMD:
                # send <NAME>[,...,<NAME>] <MESSAGE>
                if len(cmd) < 3:
                    invalidCmd(cmd[0])
                else:
                    sendTo = [s for s in re.split(self.CONV_DELIM, cmd[1])]
                    self.client.sendMessage(sendTo, cmd[2])
            elif cmd[0] == self.BCAST_CMD:
                # bcast <MESSAGE>
                if len(cmd) < 2:
                    invalidCmd(cmd[0])
                else:
                    self.client.sendMessage(['GLOBAL'], cmd[1])
            elif cmd[0] == self.EXIT_CMD:
                shutdown = True
                self.client.shutdown()

if __name__ == '__main__':
    Interface().run()