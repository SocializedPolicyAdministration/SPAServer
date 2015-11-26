# This file suppoers a Order-preserving encryption (ope).
# Reference:
#   1. http://www.cc.gatech.edu/~aboldyre/papers/bclo.pdf
import random

def getOPEKey(nLength = 2048):
    randFun = random.SystemRandom()
    n = None
    nLen = 0
    while (nLen != nLength):
        n = randFun.getrandbits(nLength)
        nLen = n.bit_length()
    return n
