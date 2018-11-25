from __future__ import print_function

sharedPrime = 23  #use zymbits random function here to produce random prime number
sharedBase = 5

alicePrivateKey = 6
bobPrivateKey = 15

# Begin
print( "Publicly Shared Variables:")
print( "    Publicly Shared Prime: " , sharedPrime )
print( "    Publicly Shared Base:  " , sharedBase )

# Alice Sends Bob A = g^a mod p
A = (sharedBase ** alicePrivateKey) % sharedPrime
print("\n  Alice Sends Over Public Chanel: ", A)


# Bob Sends Alice B = g^b mod p
B = (sharedBase ** bobPrivateKey) % sharedPrime
print("Bob Sends Over Public Chanel: ", B)

print( "\n------------\n" )
print( "Privately Calculated Shared Secret:" )
# Alice Computes Shared Secret: s = B^a mod p
aliceSharedSecret = (B ** alicePrivateKey) % sharedPrime
print( "    Alice Shared Secret: ", aliceSharedSecret )

# Bob Computes Shared Secret: s = A^b mod p
bobSharedSecret = (A**bobPrivateKey) % sharedPrime
print( "    Bob Shared Secret: ", bobSharedSecret )