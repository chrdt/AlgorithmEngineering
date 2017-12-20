from functools import wraps
from time import time
from random import randint, choice


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        return end-start
    return wrapper


def random_mac():
    return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
        randint(0, 255)
    )


if __name__ == '__main__':
    for i in range(20):
        with open("dump/" + str(i), "w") as file:
            random_macs = []
            while len(random_macs) < 256:
                mac = random_mac()
                if mac not in random_macs:
                    random_macs.append(mac)

            for _ in range(10000000):
                x = choice(random_macs)
                file.write(x + "\n")
