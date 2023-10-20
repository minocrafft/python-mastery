from decimal import Decimal


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

    @classmethod
    def from_row(cls, row):
        return cls(*[func(val) for func, val in zip(cls._types, row)])

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

    def sell(self, n):
        self.shares -= n

    def __repr__(self):
        return f"Stock({self.name}, {self.shares}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )


class DStock(Stock):
    _types = (str, int, Decimal)
