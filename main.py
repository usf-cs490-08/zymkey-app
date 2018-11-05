def serverResponse():
    return True
    # In place of an actual server with real logic.
    # Will always confirm ludicrous transactions and no security for authorization


def displayMenu():
    print("1: Check balance")
    print("2: Send currency")
    print("3: Receive currency")
    print("4: Exit")


def getBalance():
    print('TODO')
    # Call GET to server to retrieve balance using 'publicKey'


def postTransaction():
    print('TODO')
    # Post a transaction to the server to be placed in the transactionQueue


def generateAddress():
    print('TODO')
    # Generate the address to receive a transaction

def userInput():
    try:
        opt = int(input("Select an option"))

    except ValueError:
        print("Not an integer")

    else:
        if opt == 1:
            getBalance()
            #Check balance

        elif opt == 2:
            postTransaction()
            #Send moneyz

        elif opt == 3:
            generateAddress()
            #Create address to give.

        elif opt == 4:
            return False

        else:
            print("!!!!!\n Not a valid menu option\n!!!!!")


    return True


def initialize():
    # Initialize a "user" in the authorizationMap and input private key

    authMap = {1234 : '****'}

def main():
    run = True
    while run:
        displayMenu()
        run = userInput()


if __name__ == "__main__":
    main()
