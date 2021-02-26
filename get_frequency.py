from scapy.layers.dot11 import RadioTap
from scapy.all import rdpcap
import argparse


# Read a PCAP file and compare with golden answer
# This is mostly to verify the code works as intended
def test(test_pcap='test.pcapng'):
    test_freq = get_channel(2407)
    assert (test_freq == 2400)


# Source:
# https://stackoverflow.com/questions/60473359/scapy-get-set-frequency-or-channel-of-a-packet
def get_channel(frequency):
    base = 2407  # 2.4Ghz
    if frequency // 1000 == 5:
        base = 5000  # 5Ghz
    # 2.4 and 5Ghz channels increment by 5
    return (frequency - base) // 5


# Source:
# https://stackoverflow.com/questions/60473359/scapy-get-set-frequency-or-channel-of-a-packet
def get_frequency(packet):
    if hasattr(packet, 'RadioTap'):
        return packet[RadioTap].Channel
    else:
        return None


def main():
    parser = argparse.ArgumentParser(
        prog='A python program that uses scapy to get signal strength given SSID')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--test', action='store_true')
    args = parser.parse_args()

    if args.test:
        test()

    # run main
    pcap_reader = rdpcap('test.pcapng')
    for packet in pcap_reader:
        if hasattr(packet, 'RadioTap'):
            print("Has Ethernet Stuff")
            print(packet.summary())
        # print(packet.summary())
        # print(packet.show())


main()
