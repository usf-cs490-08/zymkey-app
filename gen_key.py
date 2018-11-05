import argparse
import zymkey
from textwrap import fill

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='Generate keys')
    parser.add_argument('-g', '--generate', action='store_true')
    parser.add_argument('-r', '--retrieve', action='store_true')
    parser.add_argument('filename')
    return parser.parse_args()

def gen_key(size=32, output_file='key'):
    '''
        size - number of bytes (1 byte = 8 bits)
    '''
    bits = zymkey.client.get_random(size)
    out = fill(' '.join('{:02x}'.format(c) for c in bits))
    print(out)

    encrypted = zymkey.client.lock(bits)
    
    f = open(output_file, 'w+b')
    f.write(encrypted)
    f.close()

def get_key(input_file):
    '''
       Retrieve key for cryptoprocessing
       input_file - file where the encrypted key is saved to
    '''
    f = open(input_file, 'rb')
    data = bytearray(f.read())
    f.close()
    decrypted = zymkey.client.unlock(data)
    out = fill(' '.join('{:02x}'.format(c) for c in decrypted))
    print(out)

def main():
    args = get_args()
    
    if (args.generate):
        print("Generate keys")
        print("File: " + args.filename)
        gen_key(32, args.filename)
    elif (args.retrieve):
        print("Retrieve keys")
        print("File: " + args.filename)
        get_key(args.filename)
        
if __name__ == '__main__':
    main()
