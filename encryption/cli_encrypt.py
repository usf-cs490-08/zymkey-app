import argparse
import json
import os
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

def get_args():
    ''' Argument parser '''
    parser = argparse.ArgumentParser(description='CLI encrypt')

    parser.add_argument('-i', '--identity', required=True)
    parser.add_argument('-t', '--to')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-m', '--message')
    
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-e', '--encrypt', action='store_true')
    mode.add_argument('-d', '--decrypt', action='store_true')
    mode.add_argument('-g', '--generate', action='store_true',  help='generate keys')
    
    return parser.parse_args()

def encrypt_m(sender, receiver, message):
    f = open("address.json", 'r')
    keys = json.load(f)
    ptdata = message.encode()
    ciphertext = encrypt(keys[receiver], ptdata)
    bytetolist = list(ciphertext)

    json_obj = {"from": sender, "message": bytetolist}
    json_str = json.dumps(json_obj)
    m = open("message.json", 'w')
    m.write(json_str)
    m.close()
    f.close()
    # TODO: call zymkey script to unlock json file content
    #dst = zymkey.client.unlock(src)
    #print(dst)
    
def decrypt_m(identity, message_file):
    filename = identity + ".json"
    f = open(filename, 'r')
    m = open(message_file, 'r')
    keys = json.load(f)
    json_obj = json.load(m)
    listtobyte = bytes(json_obj["message"])
    ptdata = decrypt(keys["private"], listtobyte)
    plaintext = ptdata.decode()
    print(json_obj["from"] + " says \"" + plaintext + "\"")
    f.close()


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

    f = open(filename, 'w')
    f.write(json_str)
    f.close()
    
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
        encrypt_m(args.identity, args.to, args.message)
    elif args.decrypt:
        print("decrypting")
        decrypt_m(args.identity, args.filename)
        

if __name__ == '__main__':
    main()
