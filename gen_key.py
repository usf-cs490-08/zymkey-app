import argparse
import zymkey
from textwrap import fill


def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='Generate keys')
    parser.add_argument('-g', '--generate', action='store_true')
    parser.add_argument('-r', '--retrieve', action='store_true')
    return parser.parse_args()

def gen_key(size=32):
    '''
        size - number of bytes (1 byte = 8 bits)
    '''
    bits = zymkey.client.get_random(size)
    pass

def get_key():
    pass

def main():
    args = get_args()
    
    if (args.generate):
        print("Generate keys")
    elif (args.retrieve):
        print("Retrieve keys")
        

if __name__ == '__main__':
    main()
