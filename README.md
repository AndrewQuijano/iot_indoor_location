# iot_indoor_location


## Installation
**Prerequisites**:  
This requires installing scapy, this can be taken care of by reading the requirements.txt file.

*pip install -r requirements.txt*

This was tested on Intel NUC iot device, as it supports monitor mode, which is running Ubuntu 18 LTS.  

To set up monitor mode, I used the following [guide](https://www.cellstream.com/reference-reading/tipsandtricks/410-3-ways-to-put-your-wi-fi-interface-in-monitor-mode-in-linux)

Use *ip link show* to check the interfaces. You can use the *set_monitor.sh* script to activate/deactivate monitor mode.

## Usage 
First you need to capture packets:  
tshark -i (interface) -w (file-path) -a (duration in seconds)

To verify the code is working as intended, there is a pre-configured test.pcapng, alongside the expected answer after processing in the answers.csv file. This can be tested using:  
*python3 indoor_localizer.py --test*  

If you want to use this script to analyze any arbitrary PCAP file, use the following arguments:  
*python3 indoor_localizer.py -r <PCAP-file>*  

TODO: This script will also support sniffing and creation of PCAP files rather than relying on the tshark script. This can be done as follows:  
*python3 indoor_localizer.py -s -i (interface) -t <timeout (minutes)>*


## Authors and Acknowledgment
Code Author: Andrew Quijano  
I would like to thank the Internet Real-Time (IRT) lab at Columbia University for funding this project.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Project status
TODO: First draft of specs, completed. Meet with Jan.

## References

