import re

user = None
sender = None

def displayMenu():
    print("1: Send message")
    print("2: Display history")
    print("3: Exit")


def sendMessage():
    to = input("\nsend to: ")  ## TODO clean this
    message = input("message: ")
    print("sending...")

    # TODO send via MessageSender class/entity...
    # sender.send(to, message)

def displayHistory():
    # TODO
    #  only once read from user topic offset (0 -> X) into history data structure
    #  OR
    #  print history data structure
    pass

def userInput():
    try:
        opt = int(input("Select an option: "))

    except ValueError:
        print("Not an integer")

    else:
        if opt == 1:
            sendMessage()

        elif opt == 2:
            displayHistory()

        elif opt == 3:
            return False

        else:
            print("!!!!!\n Not a valid menu option\n!!!!!")


    return True

def main():
    
    # log in
    user = input("\nusername: ")
    user = re.sub('[\s+]', '', user)  # TODO replace all characters that are invalid in a topic name
    print("\nlogged in as: %s\n" % user)

    # TODO 
    #  populate history data structure
    #  OR
    #  remember current offset (for new/old history info)

    # TODO startup 2 background threads:
    #  1. consume from user 'requested' topic & process
    #  2. consume from user 'committed' topic & process
    # https://en.wikibooks.org/wiki/Python_Programming/Threading

    # TODO setup ssh tunnel from localhost:9092 -> mcvm155:9092 (through stargate)
    # sender = MessageSender("localhost:9092")

    # run interface
    run = True
    while run:
        displayMenu()
        run = userInput()

if __name__ == "__main__":
    main()

# TODO: split into different files (& probably even repo)
from confluent_kafka import Producer
class MessageSender:

    def __init__(self, brokers):
        self.config = {'bootstrap.servers': brokers}
        self.producer = Producer(**self.conf)

    def sendMessage(self, to, message):

        def delivery_callback(err, msg):
            if err:
                print("sending error: %s" % err)
            else:
                print("message sent!")

        # TODO: decide on naming conventions
        topic = to + '-requested'

        try:
            p.produce(topic, message, callback=delivery_callback)

        except BufferError:
            print('producer queue is full (%d messages awaiting delivery): \n' % len(p))
