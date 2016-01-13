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


def add(m1, m2, n_square):
    return (m1 * m2) % n_square


def mul(m1, m2, n_square):
    return gmpy2.powmod(m1, m2, n_square)


def sub(m1, m2, n_square):
    return add(m1, mul(m2, -1, n_square), n_square)


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
        self.n_len = n_len

    def get_public_key(self):
        return [self.g, self.n]

    def get_private_key(self):
        return [self.lambda_, self.mu]
    def enc(self, m):
        r = get_primer(self.n_len)
        n_square = self.n * self.n
        a1 = gmpy2.powmod(self.g, m, n_square)
        a2 = gmpy2.powmod(r, self.n, n_square)
        return (a1 * a2) % n_square
    def dec(self, c):
        n_square = self.n * self.n
        u = gmpy2.powmod(c, self.lambda_, n_square)
        return ((u - 1) / self.n * self.mu) % self.n

paillier = Paillier(n_length=512)
a = paillier.enc(11)
b = paillier.enc(10)
b_a = sub(b, a, paillier.n * paillier.n)
print paillier.dec(b_a) - paillier.n
