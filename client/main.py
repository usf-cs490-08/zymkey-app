import re

user = None
sender = None

def displayMenu():
    print("1: Send message")
    print("2: View new messages")
    print("3: Refresh contacts")
    print("4: Generate public key")
    print("5: Exit")


def sendMessage():
    to = input("\nsend to: ")  ## TODO clean this
    message = input("message: ")
    print("sending...")

    # TODO send via MessageSender class/entity...
    # sender.send(to, message)


def newMessages():
    # TODO
    #  only once read from user topic offset (0 -> X) into history data structure
    #  OR
    #  print history data structure
    pass


def refreshContacts():
    '''
        Update local address book
        1. Consume from Kafka topic
        2. Read address book contents
        3. Unlock address book contents using Zymkey
        4. Check if username and public key already exists in address book
           a. If yes, do nothing
           b. If no, append new username and public key mapping to address book
        5. Lock updated address book contents
        6. Write locked content back into address book 
    '''
    pass


def genPublicKey():
    '''
        Generate public key for unique identification
        1. Check if public key file exists in <path to be determined>
           a. If yes, inform user that public key already exists and exit function
           b. If no, proceed to step 2 
        2. Call Zymkey module to generate public key
        3. Build JSON object that has username and public key fields
        4. Post object to "address book" topic
        5. Lock generated key bits with Zymkey
        6. Write locked key bits to <path>
    '''
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
            newMessages()
        elif opt == 3:
            refreshContacts()
        elif opt == 4:
            genPublicKey()
        elif opt == 5:
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
