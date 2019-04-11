"""Implementation of koblitz encoding and decoding"""
from ecc.utils import *
from ecc.point import Point
import math

__author__ = "Azis Adi Kuncoro"


def encode(k, n, p, a, b, message_byte):
    """Return encoded point"""
    m = encode_byte(message_byte)
    # Find solveable y
    for i in range(1, k):
        x = generate_x(m, k, i)
        y = is_y_exist(p, a, b, x)
        if (y != -1):
            break
    return Point(x, y)


def decode(k, x):
    """Return message char"""
    code = math.floor((x-1)/k)
    return decode_int(code)


def do_encoding(k, n, p, a, b, messages):
    """Do the encoding things"""
    enc_messages = [encode(k, n, p, a, b, m) for m in messages]
    return enc_messages


def do_decoding(k, message_point):
    """Do the decoding things"""
    dec_messages = [decode(k, point.x) for point in message_point]
    return dec_messages
