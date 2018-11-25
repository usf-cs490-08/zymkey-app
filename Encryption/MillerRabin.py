#python file to create unique prime numbers using Miller-Rabin
#Here we will use this class to determine the quality of our prime number

#Bigger prime numbers are hard to find

import random

#Function: will return true/false if the number is a prime number
#Args: an prime integer

lowPrimes= 

def rabinMiller(num):
    s = num -1
    t = 0

    while s%2 ==0:
        s = s//2
        t +=1

    for trials in range(5):
