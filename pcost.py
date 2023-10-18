def portfolio_cost(filename: str = "Data/portfolio.dat"):
    cost = 0

    with open(filename, "r") as f:
        for stock in f:
            try:
                name, shares, price = stock.split()
                cost += int(shares) * float(price)
            except ValueError as e:
                print(f"Couldn't parse: {stock}")
                print(f"Reason: {e}")

    return cost


if __name__ == "__main__":
    print(portfolio_cost())
