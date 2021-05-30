#!/bin/bash

# Created by Andrew Quijano
# Obtain Wireless Interface Information, Change it moinotor mode/managed mode

INT=$(sudo iw dev | sed -n '2 p' | cut -d ' ' -f2)
if [[ 'ON' == $1 ]]; then
	echo "Monitor Mode - ON"
	sudo ip link set $INT down
 	sudo iw $INT set monitor none
 	sudo ip link set $INT up
else
	echo "Monitor Mode - OFF"
	sudo ip link set $INT down
	sudo iw $INT set type managed
	sudo ip link set $INT up 
fi
