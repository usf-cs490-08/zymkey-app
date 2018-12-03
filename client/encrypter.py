import argparse, json, os
from ecies.utils import generate_eth_key, generate_key, aes_encrypt, aes_decrypt
from ecies import encrypt, decrypt


def encrypt_m(sender, receiver, message):
    f = open("address.json", 'r')
    keys = json.load(f)
    f.close()
    ptdata = message.encode()
    ciphertext = encrypt(keys[receiver], ptdata)
    return list(ciphertext)

def decrypt_m(identity, message):
    filename = identity + ".json"
    f = open(filename, 'r')
    keys = json.load(f)
    f.close()
    ptdata = decrypt(keys["private"], bytes(message))
    plaintext = ptdata.decode()

def encrypt_s(pt):
    f = open('.key', 'rb')
    shared = f.read()
    f.close()
    return aes_encrypt(shared, pt)

def decrypt_s(ct):
    f = open('.key', 'rb')
    shared = f.read()
    f.close()
    return aes_decrypt(shared, ct)
