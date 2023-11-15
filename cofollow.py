# cofollow.py
# Decorator for coroutine functions
import os
import time
from functools import wraps


# Data source
def follow(filename, target):
    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line != "":
                target.send(line)
            else:
                time.sleep(0.1)


def consumer(func):
    @wraps(func)
    def start(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f

    return start


# Sample coroutine
@consumer
def printer():
    while True:
        item = yield  # Receive an item sent to me
        print(item)


# Example use
if __name__ == "__main__":
    follow("Data/stocklog.csv", printer())
