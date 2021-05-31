# https://github.com/secdev/scapy/blob/master/scapy/layers/dot11.py#L306-L568
# https://scapy.readthedocs.io/en/latest/api/scapy.layers.dot11.html

import argparse
import pyshark


def read_test_answers():
    answer_key = dict()
    with open('answers.csv', 'r') as fd:
        # Skip Header
        next(fd)
        for line in fd:
            line = line.strip().split(',')
            transmitter_address = line[0]
            # Tree-Based, Max-CST Metric, Spanning Tree
            answer_key[transmitter_address] = (int(line[1]), int(line[2]), int(line[3]),
                                               line[4], line[5], line[6])
    return answer_key


# Read a PCAP file and compare with golden answer stored in a CSV
# This is mostly to verify the code works as intended
def test(test_pcap='test.pcapng'):
    answers = read_test_answers()
    network_data = process_pcap(test_pcap)
    for transmitter, obtained_values in network_data.items():
        gold_answer = answers[transmitter]
        for test_answer, true_answer in zip(obtained_values, gold_answer):
            print(test_answer, true_answer)
            # assert test_answer == true_answer


def write_to_csv(output_data):
    with open('output.csv', 'w+') as fd:
        # Write the headers
        fd.write('Transmitter_MAC,Is_Access_Point,strongest_rssi,frequency,sniff_time,BSSID,SSID\n')
        for transmitter, value in output_data.items():
            fd.write(transmitter + ',')
            row = ""
            for element in value:
                row += str(element) + ','
            row = row[:-1]
            fd.write(row + '\n')


def process_pcap(pcap_file):
    network_data = dict()
    with pyshark.FileCapture(pcap_file) as packets:
        for packet in packets:
            # print(packet['WLAN'])
            # print(packet['RADIOTAP'])
            # print(packet['WLAN_RADIO'])
            # print(packet['WLAN.MGT'])

            try:
                transmitter = packet['WLAN'].get_field_by_showname("Transmitter address")
            except KeyError:
                continue

            if transmitter is None:
                continue

            # 2) A flag indicating if the device is an AP or client
            is_ap = int(packet['WLAN'].get_field_by_showname("Type/Subtype")) == 8

            # 3) The strongest received signal strength (antenna signal in dBm)
            # observed from the device on each antenna
            dbm = packet['WLAN_RADIO'].get_field_by_showname("Signal strength (dBm)")

            # 4) Channel frequency of the strongest packet
            frequency = packet['RADIOTAP'].get_field_by_showname("Channel frequency")

            # 5) The timestamp of the strongest packet
            sniff_time = packet.sniff_time

            # 6) BSS id of the strongest packet
            bssid = packet['WLAN'].get_field_by_showname("BSS Id")
            print(is_ap)
            print(dbm)
            print(frequency)
            print(sniff_time)
            print(bssid)

            try:
                ssid = packet['WLAN.MGT'].get_field_by_showname("SSID")
                print(ssid)
            except KeyError:
                ssid = None

            info = [is_ap, dbm, frequency, sniff_time, bssid, ssid]
            if transmitter in network_data:
                old_data = network_data[transmitter]
                if dbm > old_data[1]:
                    network_data[transmitter] = info
            else:
                print("Found new Transmitter Address: " + transmitter)
                network_data[transmitter] = info
    return network_data


def main():
    parser = argparse.ArgumentParser(
        prog='A python program that uses scapy to get signal strength given SSID')

    parser.add_argument('-r', '--read', dest='pcap', action='store', help='input PCAP file')
    parser.add_argument('-i', '--interface', dest='interface', action='store',
                        help='Interface for Wireshark to Listen on for IoT stuff')
    parser.add_argument('-t', '--timeout', dest='timeout', action='store', type=int,
                        help='How much time the interface should be sniffed for.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--test', '-t', dest='test',
                       action='store_true', help='Test the code on given PCAPs '
                                                 'to ensure it gives the expected results')
    args = parser.parse_args()

    # Sniff if needed...
    # capture = pyshark.LiveCapture(interface=args.interface)
    # capture.sniff(timeout=10)

    if args.test:
        print("Running Test...")
        # test()
        exit(0)

    # Might be good idea to know My own MAC Address in code as well...
    network = process_pcap(args.pcap)

    for key, value in network.items():
        print(key)
        print(value)
    write_to_csv(network)


main()
