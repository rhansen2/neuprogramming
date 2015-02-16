#!/usr/bin/python

# Reads ip prefixes from stdin and creates a list of ips and outputs them to
# the file specified in the command
import sys, socket, struct

IP_BITS = 32
IP_MAX = 0xffffffff

def prefixToInt(prefix):
    octets = prefix.split('.')
    value = 0;
    value = value | (int(octets[0]) << 24)
    value = value | (int(octets[1]) << 16)
    value = value | (int(octets[2]) << 8)
    return value


def processPrefix(prefix):
    split = prefix.split('/')
    network = split[0]
    mask = int(split[1])
    networkVal = prefixToInt(network)
    minVal = 0
    maxVal = (IP_MAX >> mask)
    for i in range(minVal, maxVal + 1):
        currentIp = networkVal + i
        print socket.inet_ntoa(struct.pack('>L', currentIp))

for line in sys.stdin:
    prefixes = line.split(' ')
    for prefix in prefixes:
        processPrefix(prefix)
