#!/bin/bash

INT=$(sudo iw dev | sed -n '2 p' | cut -d ' ' -f2)
MINUTES=$1
SECONDS=$(echo $(($MINUTES*60)))
DATE=$(date +"%m-%d-%Y")

echo "Will Sniff for $SECONDS seconds..."

OUTPUT="/home/irt/iot_indoor_location/$DATE.pcapng"
echo $OUTPUT
tshark -i $INT -w /home/irt/iot_indoor_location/irt_test.pcapng -a duration:$SECONDS
