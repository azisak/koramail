"""Point module"""

__author__ = "Azis Adi Kuncoro"


class classproperty(object):
    def __init__(self, f):
        self.f = classmethod(f)

    def __get__(self, *a):
        return self.f.__get__(*a)()


class Point(object):
    def __init__(self, x, y):
        """ Point class
        Attributes
            x: axis position
            y: ordinat position
        """
        self.x = x
        self.y = y

    @classproperty
    def INFINITY(self):
        return Point(-1, -1)

    def is_infinity(self):
        return (self.x == -1 and self.y == -1)

    def __str__(self):
        return "{}, {}".format(self.x, self.y)

    def __repr__(self):
        return "{}, {}".format(self.x, self.y)
