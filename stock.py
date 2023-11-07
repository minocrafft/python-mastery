from decimal import Decimal
from validate import PositiveInteger, PositiveFloat, String


def print_portfolio(portfolio):
    print(f"{'name':>10} {'shares':>10} {'price':>10}")
    print(f"{'-'*10} {'-'*10} {'-'*10}")

    for s in portfolio:
        print(f"{s.name:>10s} {s.shares:10d} {s.price:10.2f}")


class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        return cls(*[func(val) for func, val in zip(cls._types, row)])

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, n):
        self.shares -= n

    def __repr__(self):
        # Note: The !r format code produces the repr() string
        return f"{type(self).__name__}({self.name!r}, {self.shares!r}, {self.price!r})"

    def __setattr__(self, name, value):
        if name not in {"name", "shares", "price"}:
            raise AttributeError("No attribute %s" % name)
        super().__setattr__(name, value)

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )


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
