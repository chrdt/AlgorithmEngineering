import argparse
import random

import abc
import os

import sys
from scapy.all import *
from scapy.layers.l2 import Ether, ARP, Dot3
from scapy.utils import PcapNgReader, wrpcap


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
        print "{},cnt,avg len".format(self.frame_groups)
        for _frame_group in self._avg_frame_len:
            self._avg_frame_len[_frame_group] /= self._frame_count[_frame_group]
            print "{},{},{}".format(",".join(map(str, _frame_group)),
                                    self._frame_count[_frame_group],
                                    self._avg_frame_len[_frame_group])

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


class DumpFrame(PCAPProcessing):
    """
    dump frame to console
    """

    def finalize(self):
        pass

    def process(self, frame):
        frame.show()


def _process_file(input_file, actions):
    frm_num = 0
    with PCapReader(input_file) as reader:

        for frame in reader.get_frame():

            frm_num += 1
            # frame.show()
            # print 'process frame {}...'.format(frm_num)
            for action in actions:
                action.process(frame)

    for action in actions:
        action.finalize()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
                                     'Analyse and rework pcap traces')

    parser.add_argument('input',
                        help='input file to be processed')
    parser.add_argument('--output', '-o',
                        help='an integer for the accumulator')
    parser.add_argument('--extract-mac-addresses', '-x',
                        help='extract list of all MAC addresses to given file')
    parser.add_argument('--average-frame-length', '-f',
                        help='calculate the average frame length grouped by the given'
                             ' attributes (None, TCP-Port, Ethernet-Type)'
                             ', for example -f TCP-Port,Ethernet-Type')
    parser.add_argument('--dump', '-d', action='store_true',
                        help='dump frames to console')

    args = parser.parse_args()
    print args
    if not os.path.exists(args.input):
        sys.stderr.writelines('file not found: {}\nabort.\n'.format(args.input))
        sys.exit(1)

    actions = []

    if args.average_frame_length:
        actions.append(AverageFrameLength(args.average_frame_length))

    if args.extract_mac_addresses:
        actions.append(ExtractMACAddresses(args.extract_mac_addresses))

    if args.dump:
        actions.append(DumpFrame())
        
    if args.output:
        actions.append(PcapOutput(args.output))

    _process_file(args.input, actions)
