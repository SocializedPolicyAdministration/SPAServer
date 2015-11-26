# This program supports paillier encryption.
# Reference:
#   1. http://www.gemplus.com/smart/rd/publications/pdf/Pai99pai.pdf
#   2. https://en.wikipedia.org/wiki/Paillier_cryptosystem
#   3. https://github.com/NICTA/python-paillier
import random
import math

import gmpy2


def get_primer(n):
    """Return a random n-bit prime number"""
    rand_fun = random.SystemRandom()
    r = gmpy2.mpz(rand_fun.getrandbits(n))
    r = gmpy2.bit_set(r, n - 1)
    return int(gmpy2.next_prime(r))


class Paillier(object):
    """A class support paillier encryption"""
    def __init__(self, n_length=512):
        n_len = 0
        p = None
        q = None
        n = None
        while n_len != n_length:
            p = get_primer(n_length // 2)
            q = get_primer(n_length // 2)
            n = p * q
            n_len = n.bit_length()

        g = n + 1
        p_sub_one = p - 1
        q_sub_one = q - 1

        phi_n = p_sub_one * q_sub_one
        lambda_ = phi_n
        mu = int(gmpy2.invert(phi_n, n))
        self.g = g
        self.n = n
        self.lambda_ = lambda_
        self.mu = mu

    def get_public_key(self):
        return [self.g, self.n]

    def get_private_key(self):
        return [self.lambda_, self.mu]
