#!/usr/bin/env python2
from __future__ import print_function
import argparse
import abc

from scapy.all import *
from scapy.layers.l2 import Ether, ARP, Dot3
from scapy.utils import PcapNgReader, wrpcap
from src.hashtables.bucketized_cuckoo_hashing import BucketizedCuckooHash
from src.hashtables.cuckoo_hashing import CuckooHash
from src.util.timer import timer
from time import time


class PCAPProcessing(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def process(self, frame):
        pass

    @abc.abstractmethod
    def finalize(self):
        pass


class PCapReader:
    def __init__(self, filename):
        self.reader = PcapNgReader(filename)

    def __enter__(self):
        return self

    def get_frame(self):
        try:
            while True:
                frm = self.reader.read_packet()

                if frm:
                    yield frm
                else:
                    return
        except:
            return

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class AverageFrameLength(PCAPProcessing):
    """
    calculate average frame length applying given filters
    """

    def finalize(self):
        print("{},cnt,avg len".format(self.frame_groups))
        for _frame_group in self._avg_frame_len:
            self._avg_frame_len[_frame_group] /= self._frame_count[_frame_group]
            print("{},{},{}".format(",".join(map(str, _frame_group)),
                                    self._frame_count[_frame_group],
                                    self._avg_frame_len[_frame_group]))

    def process(self, frame):
        _group_attributes = ()


        for func in self._group_funcs:
            try:
                _group_attributes += (func(frame),)
            except IndexError:
                _group_attributes += ("",)

        if _group_attributes in self._avg_frame_len:
            self._avg_frame_len[_group_attributes] += len(frame)
            self._frame_count[_group_attributes] += 1
        else:
            self._avg_frame_len[_group_attributes] = len(frame)
            self._frame_count[_group_attributes] = 1

    def __init__(self, frame_groups):
        self._group_functions = {
            "Ethernet-Type": lambda frame: '0x{:04x}'
                .format(int(frame[Ether].type)),
            "TCP-Port": lambda frame: frame[TCP].sport,
            "None": lambda frame: "all"
        }

        self.frame_groups = frame_groups
        self._group_funcs = [self._group_functions[arg]
                             for arg in frame_groups.split(",")]
        self._avg_frame_len = {}
        self._frame_count = {}


class PcapOutput(PCAPProcessing):
    """
    write frames to given file
    """

    def finalize(self):
        pass

    def process(self, frame):
        wrpcap(self._filename, frame, append=True)

    def __init__(self, filename):
        self._filename = filename


class ExtractMACAddresses(PCAPProcessing):
    """
    write distinct MAC addresses found in frames to given file
    """

    def finalize(self):
        with open(self._filename, 'w') as o_file:
            for mac in self._mac_addresses:
                o_file.write('{}\n'.format(mac))

    def process(self, frame):

        try:
            src_mac = frame[Ether].src
            dst_mac = frame[Ether].dst
        except IndexError:
            try:
                src_mac = frame[Dot3].src
                dst_mac = frame[Dot3].dst
            except IndexError:
                return

        if src_mac not in self._mac_addresses:
            self._mac_addresses[src_mac] = ''
        if dst_mac not in self._mac_addresses:
            self._mac_addresses[dst_mac] = ''

    def __init__(self, filename):
        self._filename = filename
        self._mac_addresses = {}


class InsertHashTable():
    """
    the actual class, that is used for this project
    others are used for further analyzation of pcaps
    """
    def finalize(self):
        print("Done:" + str(self.insertion_time))

    def process(self, frame):
        start = time()
        try:
            src_mac = frame[Ether].src
        except IndexError:
            try:
                src_mac = frame[Dot3].src
            except IndexError:
                return


        mac_as_int = int(src_mac.translate(None, ":.-"), 16)
        if not self.hashtable.contains(mac_as_int):
            self.hashtable.insert(mac_as_int, 1)
        self.insertion_time += time()-start

    def __init__(self):
        self.hashtable = CuckooHash(8)
        self.insertion_time = 0


class DumpFrame(PCAPProcessing):
    def finalize(self):
        pass

    def process(self, frame):
        frame.show()


@timer
def _process_file(input_file, actions):
    with PCapReader(input_file) as reader:
        for frame in reader.get_frame():
            for action in actions:
                action.process(frame)

    for action in actions:
        action.finalize()


if __name__ == '__main__':
    """
    TODO: re-implement argparse to be able to chain differenct actions
    """

    basic_path = "../../benchmarks/pcapReal/4SICS-GeekLounge-151022.pcap"

    if not os.path.exists(basic_path):
        sys.stderr.writelines('file not found: {}\nabort.\n'.format(basic_path))
        sys.exit(1)

    actions = [InsertHashTable()] # only one action for this project
    runtime = _process_file(basic_path, actions)
    print(runtime)
