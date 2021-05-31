# iot_indoor_location


## Installation
**Prerequisites**:  
This requires installing scapy, this can be taken care of by reading the requirements.txt file.

*pip install -r requirements.txt*

As this script is looking for the RadioTap attribute, which requires some extra [configuration](https://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode  
).  

This was tested on Intel NUC iot device, as it supports monitor mode, which is running Ubuntu 18 LTS.  

To set up monitor mode, I used the following 
[guide](https://www.cellstream.com/reference-reading/tipsandtricks/410-3-ways-to-put-your-wi-fi-interface-in-monitor-mode-in-linux)

Use *ip link show* to check the interfaces.

## Usage 
First you need to capture packets:  
tshark -i wlp58s0 -w /home/irt/irt_test.pcapng -a duration:60

There is a test.pcapng is used to verify the functionality.  

The script uses scapy to access [RadioTap](https://stackoverflow.com/questions/60473359/scapy-get-set-frequency-or-channel-of-a-packet) headers. 
A complete list of all values that can be captured is found [here](https://www.wireshark.org/docs/dfref/r/radiotap.html)

## Authors and Acknowledgment
Code Author: Andrew Quijano  
I would like to thank the Internet Real-Time (IRT) lab at Columbia University for funding this project.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Project status
Currently I am working on getting the basics of capturing Radio.

## References

