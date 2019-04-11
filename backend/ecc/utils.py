""" Utils for ecc"""
import functools
import time
import random
import os

from ecc.point import Point

__author__ = "Azis Adi Kuncoro"


def timer(func):
    """Record elapsed time in a function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        t = time.time()
        func(*args, **kwargs)
        print("[%s] Elapsed %.6f second" % (func.__name__, time.time()-t))
        return func(*args, **kwargs)
    return wrapper_timer


def modInverse(x, p):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        print("X: {}, P:{}".format(x, p))
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)


def y_square(p, a, b, x):
    """Compute y^2 in form x^3+ax+b mod p
    """
    return (x**3+a*x+b) % p


def is_y_exist(p, a, b, x):
    """Check whether any y exists for given x in ECC
    Returns:
        -1 is not exists, a number otherwise
    """
    y_sqr = y_square(p, a, b, x)
    for i in range(p):
        if ((i*i) % p == y_sqr):
            return i
    return -1


def encode_char(character):
    """Encoding character to an integer"""
    return 10 + ord(character.lower())-ord('a')


def decode_code(code):
    """Decoding integer to a character"""
    return chr(ord('a') + code-10)


def encode_byte(b):
    """Encoding byte to integer repr"""
    return int(b)


def decode_int(code):
    """Decoding int to byte repr"""
    # print("Code: ",code)
    return bytes([code])


def generate_x(m, k, offset):
    """Yielding x by a function"""
    return m*k+offset


def generate_public_key(file_name, ecc, basis_point, private_key):
    pub = ecc.iteration(basis_point, private_key)
    to_write = "{},{}".format(pub.x, pub.y)
    if not os.path.exists('keys'):
        os.makedirs('keys')
    f_path = "keys/{}".format(file_name)
    with open(f_path, "w") as f:
        f.write(to_write)
        f.close()
        print("created ", f_path)


def generate_private_key(file_name, n):
    pri = random.randint(1, n)
    if not os.path.exists('keys'):
        os.makedirs('keys')
    f_path = "keys/{}".format(file_name)
    with open(f_path, "w") as f:
        f.write(str(pri))
        f.close()
        print("created ", f_path)
    return pri


def generate_keys(key_name, ecc, basis_point, n):
    pri = generate_private_key("{}.pri".format(key_name), n)
    generate_public_key("{}.pub".format(key_name), ecc, basis_point, pri)


def read_public_key(file_path):
    with open(file_path, "r") as f:
        pub = f.read()
        f.close()
        pub = pub.split(",")
        return Point(int(pub[0]), int(pub[1]))


def read_private_key(file_path):
    with open(file_path, "r") as f:
        pri = f.read()
        f.close()
        return int(pri)


def generate_out_file(file_byte, file_path):
    with open(file_path, "wb") as f:
        f.write(file_byte)
        f.close()
        print("Succesfully written to ", file_path)
