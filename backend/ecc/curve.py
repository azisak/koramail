"""Implementation of Eliptic curve cryptography"""

from ecc.utils import *
from ecc.koblitz import *
from ecc.point import Point

__author__ = "Azis Adi Kuncoro"


class ECC(object):
    def __init__(self, a, b, p, k, n):
        self.a = a
        self.b = b
        self.p = p
        self.k = k
        self.n = n

    def get_y_square(self, x):
        """Return y_square of x"""
        return (x**3 + self.a*x + self.b) % self.p

    def is_on_curve(self, point):
        """Check whether a point is on curve"""
        return (point.y**2 % self.p) == self.get_y_square(point.x)

    def subtract(self, point_p, point_q):
        """Subtract two points in ECC (P - Q)
        Return
            {Point} point as a subtraction result 
        """
        if (point_p.is_infinity()):
            return point_q
        if (point_q.is_infinity()):
            return point_p
        if (point_p.x == point_q.x and point_p.y == point_q.y):
            return Point.INFINITY

        p_q_new = Point(point_q.x, (-point_q.y) % self.p)
        return self.add(point_p, p_q_new)

    def add(self, point_p, point_q):
        """Sum two points in ECC (P + Q)
        Return
            {Point} point as an addition result
        """
        if (point_p.is_infinity()):
            return point_q
        if (point_q.is_infinity()):
            return point_p

        if (point_p.x == point_q.x and point_p.y == point_q.y):
            if (point_p.y == 0):
                return Point.INFINITY
            grad = (3*(point_p.x**2) + self.a) * \
                modInverse(2*point_p.y, self.p)
            grad = int(grad) % self.p
            x_r = (grad**2 - point_p.x - point_q.x) % self.p
            y_r = (grad*(point_p.x - x_r) - point_p.y) % self.p
            return Point(x_r, y_r)
        else:
            grad = (point_p.y - point_q.y) * \
                modInverse(point_p.x - point_q.x, self.p)
            grad = grad % self.p
            x_r = (grad**2 - point_p.x - point_q.x) % self.p
            y_r = (grad*(point_p.x - x_r) - point_p.y) % self.p
            return Point(x_r, y_r)

    def encrypt_message(self, message, point_basis, public_key):
        """Encrypting message using ecc

        Arguments:
            message {Bytes}
            point_basis {Point}
            public_key {Point}

        Returns:
            {String} -- Encrypted message
        """
        encoded_messages = do_encoding(
            self.k, self.n, self.p, self.a, self.b, message)
        encrypted_messages = []
        for point_message in encoded_messages:
            temp = self.iteration(point_basis, self.k)
            encrypted_messages.append(temp.x)
            encrypted_messages.append(temp.y)
            temp = self.add(point_message, self.iteration(public_key, self.k))
            encrypted_messages.append(temp.x)
            encrypted_messages.append(temp.y)

        encrypted_messages = str(encrypted_messages)[1:-1].replace(" ", "")
        return encrypted_messages

    def decrypt_message(self, encrypted_messages, private_key):
        """Decrypt message using ecc

        Arguments:
            encrypted_messages {String} 
            private_key {int} 

        Returns:
            {Bytes} -- message after decryption
        """

        encrypted_messages = [int(m) for m in encrypted_messages.split(',')]
        decrypted_messages = []
        for i in range(0, len(encrypted_messages), 4):
            decrypted_messages.append(self.subtract(
                Point(encrypted_messages[i+2], encrypted_messages[i+3]),
                self.iteration(
                    Point(encrypted_messages[i], encrypted_messages[i+1]), private_key)
            ))

        decoded_messages = (do_decoding(self.k, decrypted_messages))
        out_msg = b"".join(decoded_messages)
        return out_msg

    def create_basis_point(self):
        """Generating basis point"""
        x = -1
        y = -1
        while (y == -1):
            x += 1
            y = is_y_exist(self.p, self.a, self.b, x)
        return Point(x, y) if (y != -1) else Point.INFINITY

    def iteration(self, point_p, k):
        """Doiint iteration point_p*k"""
        if k >= 2:
            p = self.add(point_p, point_p)
            for i in range(k-2):
                p = self.add(p, point_p)
            return p
        elif k == 1:
            return point_p
        else:
            print("Unhandled k = ", k)