# iot_indoor_location
[![Build Status](https://www.travis-ci.com/AndrewQuijano/iot_indoor_location.svg?branch=main)](https://www.travis-ci.com/AndrewQuijano/iot_indoor_location)
[![codecov](https://codecov.io/gh/AndrewQuijano/iot_indoor_location/branch/main/graph/badge.svg?token=8UNDO3DR82)](https://codecov.io/gh/AndrewQuijano/iot_indoor_location)

## Installation
**Prerequisites**:  
This requires installing scapy, this can be taken care of by reading the requirements.txt file.

*pip install -r requirements.txt*

This was tested on Intel NUC iot device, as it supports monitor mode, which is running Ubuntu 18 LTS.  

To set up monitor mode, I used the following [guide](https://www.cellstream.com/reference-reading/tipsandtricks/410-3-ways-to-put-your-wi-fi-interface-in-monitor-mode-in-linux)  
You can use the *set_monitor.sh* script to activate/deactivate monitor mode.

## Usage
To verify the code is working as intended, there is a pre-configured test.pcapng, alongside the expected answer after processing in the answers.csv file. This can be tested using:  
*python3 indoor_localizer.py --test*  

If you want to use this script to analyze any arbitrary PCAP file, use the following arguments:  
*python3 indoor_localizer.py -r (PCAP-file)*  

This script also supports sniffing packets and dumping into a PCAP. This can be done as follows:  
*python3 indoor_localizer.py -s -i (interface) -t (timeout in minutes) -c (number of packets to sniff)*


## Authors and Acknowledgment
Code Author: Andrew Quijano  
I would like to thank the Internet Real-Time (IRT) Lab at Columbia University for funding this project.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Project status
TODO: First draft of specs are completed. Will have code reviewed by Jan and discuss next steps.

## References

