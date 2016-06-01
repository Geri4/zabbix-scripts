#!/usr/bin/env python

## Script for monitoring quagga bgp peers ##
import telnetlib, re, sys, os

## Constants ##
BGPD_HOST='127.0.0.1'
BGPD_PORT=2605
BGPD_PASSWORD='zebra'

def show_usage(message, code = 1):
    print message
    print "Usage: %s peer-ip-address" % sys.argv[0]
    sys.exit(code)

if len(sys.argv) != 2:
    show_usage("Error: peer ip address is required")

validaddress = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1])
if not validaddress:
    print 'Error: wrong ip address'
    sys.exit(1)
else:
    peer = sys.argv[1]

tn = telnetlib.Telnet(BGPD_HOST, BGPD_PORT)
tn.read_until("Password: ")
tn.write(BGPD_PASSWORD+'\n')
tn.read_until("> ")
tn.write('sh ip bgp summary\n')
text = tn.read_until("> ")
peerline = re.search(r'\n'+peer+r'\s.*\r', text)
if peerline:
    peerstatus = re.findall(r'\w+', peerline.group())[-1]
    try:
        peerstatus == int(peerstatus)
    except ValueError:
        peerstatus = 0
    print peerstatus
else:
    print 'Error: peer not found'
