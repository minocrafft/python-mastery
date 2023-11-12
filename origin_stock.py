from decimal import Decimal
from validate import PositiveInteger, PositiveFloat, String


def print_portfolio(portfolio):
    print(f"{'name':>10} {'shares':>10} {'price':>10}")
    print(f"{'-'*10} {'-'*10} {'-'*10}")

    for s in portfolio:
        print(f"{s.name:>10s} {s.shares:10d} {s.price:10.2f}")


class Stock:
    __slots__ = ("name", "_shares", "_price")
    _types = (str, int, float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        # Note: The !r format code produces the repr() string
        return f"{type(self).__name__}({self.name!r}, {self.shares!r}, {self.price!r})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Expected {self._types[1].__name__}")
        if value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected {self._types[2].__name__}")
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


class DStock(Stock):
    _types = (str, int, Decimal)


class SimpleStock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price


class Readonly:
    def __init__(self, obj):
        self.__dict__["_obj"] = obj

    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute")

    def __getattr__(self, name):
        return getattr(self._obj, name)
