from functools import wraps
from time import time


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        return end-start
    return wrapper
