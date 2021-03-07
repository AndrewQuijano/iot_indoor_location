#!/bin/bash

sudo ip link set $1 down
sudo iw $1 set monitor none
sudo ip link set $1 up
