import argparse
import json
import os
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='CLI encrypt')

    parser.add_argument('-i', '--identity', required=True)
    
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-e', '--encrypt', action='store_true')
    mode.add_argument('-d', '--decrypt', action='store_true')
    mode.add_argument('-g', '--generate', action='store_true',  help='generate keys')
    
    return parser.parse_args()

def encrypt(identity, message):
    filename = identity + ".json"
    f = open(filename, 'rb')

    #src = f.read()
    f.close()
    # TODO: call zymkey script to unlock json file content
    #dst = zymkey.client.unlock(src)
    #print(dst)
    
    pass

def decrypt(identity, message):
    pass

def gen_key(identity):
    filename = identity + ".json"
    if (os.path.exists(filename)):
        print("Keys already generated!")
        return

    eth_key = generate_eth_key()
    prv_key = eth_key.to_hex()
    pub_key = eth_key.public_key.to_hex()
    json_obj = {"user": identity, "private": prv_key, "public": pub_key}
    json_str = json.dumps(json_obj)

    # TODO: Call zymkey script to lock json_str
    
    #f = open(filename, 'wb')
    
    #f.close()

def main():
    args = get_args()

    if args.generate:
        print('generate keys')
        gen_key(args.identity)
    if args.encrypt:
        print("encrypting")
    elif args.decrypt:
        print("decrypting")
        

if __name__ == '__main__':
    main()
