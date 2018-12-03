import argparse
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='CLI encrypt')
    parser.add_argument('file')
    parser.add_argument('-i', '--identity')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-e', '--encrypt', action='store_true')
    mode.add_argument('-d', '--decrypt', action='store_true')
    
    return parser.parse_args()

def encrypt():

    pass

def decrypt():
    pass


def main():
    args = get_args()
    pass

if __name__ == '__main__':
    main()
