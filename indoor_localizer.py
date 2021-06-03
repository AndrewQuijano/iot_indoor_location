# https://github.com/secdev/scapy/blob/master/scapy/layers/dot11.py#L306-L568
# https://scapy.readthedocs.io/en/latest/api/scapy.layers.dot11.html

import argparse
import datetime
import pyshark
from asyncio import TimeoutError


# Helper function to read 'answers.csv'
# This is used for testing the code works as intended.
def read_test_answers():
    answer_key = dict()
    with open('answers.csv', 'r') as fd:
        # Skip Header
        next(fd)
        for line in fd:
            line = line.strip().split(',')
            transmitter_address = line[0]

            # Determine if it was an AP or not
            if line[1].lower() == 'true':
                answer_key[transmitter_address] = [True, line[2], line[3],
                                                   line[4], line[5], line[6]]
            else:
                answer_key[transmitter_address] = [False, line[2], line[3],
                                                   line[4], line[5], line[6]]
    return answer_key


# Read a PCAP file and compare with golden answer stored in a CSV
# This is to verify the code works as intended
def test(test_pcap='test.pcapng'):
    answers = read_test_answers()
    network_data = process_pcap(test_pcap)
    for transmitter, obtained_values in network_data.items():
        gold_answer = answers[transmitter]
        # print("Comparing answer for Device: " + transmitter)
        # print(gold_answer)
        # print(obtained_values)
        for test_answer, true_answer in zip(obtained_values, gold_answer):
            # Skip date, bc who cares about that...
            # print(test_answer, true_answer)
            # print(type(test_answer), type(true_answer))
            if not isinstance(test_answer, datetime.datetime):
                assert test_answer == true_answer


# Print the output of analysis to CSV file
# This was used to create answers.csv for test.pcapng
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
            try:
                ssid = packet['WLAN.MGT'].get_field_by_showname("SSID")
            except KeyError:
                ssid = ''

            if bssid is None:
                bssid = ''
            if ssid is None:
                ssid = ''
            ssid = ssid.strip()
            # print(is_ap)
            # print(dbm)
            # print(frequency)
            # print(sniff_time)
            # print(bssid)
            # print(ssid)

            info = [is_ap, dbm, frequency, sniff_time, bssid, ssid]
            if transmitter in network_data:
                old_data = network_data[transmitter]
                # If it was AP before, please preserve it
                if old_data[0]:
                    info[0] = True

                    # -60 is stronger than -70 dBM
                    # If a better reading received, replace old reading entirely.
                    if dbm > old_data[1]:
                        network_data[transmitter] = info
                    else:
                        network_data[transmitter] = old_data
                else:
                    # If it was detected as an AP now, this should be preserved as well.
                    if is_ap:
                        old_data[0] = True
                        # -60 is stronger than -70 dBM
                        # If a better reading received, replace old reading entirely.
                        if dbm > old_data[1]:
                            network_data[transmitter] = info
                        else:
                            network_data[transmitter] = old_data
            else:
                print("Found new Transmitter Address: " + transmitter)
                network_data[transmitter] = info
    return network_data


def progress_bar(packet):
    print(packet)


def sniff(args):
    if args.interface is None:
        print("No Interface Provided...Closing now...")
        return

    if args.output is None:
        capture = pyshark.LiveCapture(interface=args.interface, output_file='irt_test.pcapng')
    else:
        capture = pyshark.LiveCapture(interface=args.interface, output_file=args.output)

    try:
        if args.timeout is None:
            capture.apply_on_packets(progress_bar, timeout=60)
            # capture.sniff(timeout=60)
        else:
            capture.apply_on_packets(progress_bar, timeout=args.timeout * 60)
            # capture.sniff(timeout=args.timeout * 60)
    except TimeoutError:
        print("Packet Capture completed...")
    # capture.clear()
    capture.close()


def main():
    parser = argparse.ArgumentParser(
        prog='A python program that uses scapy to get signal strength given SSID')

    parser.add_argument('-i', '--interface', dest='interface', action='store',
                        help='Interface for Wireshark to Listen on for IoT stuff', type=str)
    parser.add_argument('-t', '--timeout', dest='timeout', action='store', type=int,
                        help='How much time (in minutes), the interface should be sniffed for.')
    parser.add_argument('-o', '--output', dest='output', action='store', type=str,
                        help='Destination for output PCAP file')
    parser.add_argument('-c', '--count', dest='count', action='store', type=int,
                        help='Number of Packets until sniffer stops sniffing...')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--test', dest='test',
                       action='store_true', help='Test the code on given PCAPs '
                                                 'to ensure it gives the expected results')
    group.add_argument('-r', '--read', dest='pcap', action='store', help='input PCAP file', type=str)
    group.add_argument('-s', '--sniff', dest='sniff',
                       action='store_true', help='Test the code on given PCAPs '
                                                 'to ensure it gives the expected results')
    args = parser.parse_args()

    if args.sniff:
        print("Started sniffing...")
        sniff(args)
        exit(0)

    if args.test:
        print("Running Test...")
        test()
        exit(0)

    network = process_pcap(args.pcap)

    for key, value in network.items():
        print(key)
        print(value)
    write_to_csv(network)


main()
