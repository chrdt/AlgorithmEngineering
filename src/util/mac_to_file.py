#!/usr/bin/env python2

from random import randint, choice


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
    for j in range(2,11,2):
        for i in range(20):
            with open("../../benchmarks/pcapSim/medium/{}M/".format(j) + str(i), "w") as file:
                random_macs = []
                while len(random_macs) < 512:
                    mac = random_mac()
                    if mac not in random_macs:
                        random_macs.append(mac)

                for _ in range(j*1000000):
                    x = choice(random_macs)
                    file.write(x + "\n")
