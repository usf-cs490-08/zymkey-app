from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k = generate_eth_key()
prvhex = eth_k.to_hex()
pubhex = eth_k.public_key.to_hex()

message = "this is a test"
ptdata = message.encode()
ciphertext = encrypt(pubhex, ptdata)


#print(ciphertext)
bytetolist = list(ciphertext)
#print(bytetolist)
listtobyte = bytes(bytetolist)

#ptdata  = decrypt(prvhex, ciphertext)
ptdata  = decrypt(prvhex, listtobyte)
plaintext = ptdata.decode()

print(plaintext)
print(type(plaintext))
