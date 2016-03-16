#!/usr/bin/python
import socket

#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("gmail.com",80))
#Address = (s.getsockname()[0])
#s.close()

import urllib
import re

print "we will try to open this url, in order to get IP Address"
url = "http://checkip.dyndns.org"
print url
request = urllib.urlopen(url).read()
theIP = re.findall(r"d{1,3}.d{1,3}.d{1,3}.d{1,3}", request)
print "your IP Address is: ",  theIP


print "Enter User Name"
Prompt = '>'
UserName = raw_input(Prompt)

print "Connect to?"
ConnectTo = raw_input(Prompt)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerAddr = "67.241.38.178" 
Port = 5000

s.connect((ServerAddr, Port))
Incomming = s.recv(1024)
print Incomming
s.send(Address)
print "Address sent"
s.send(UserName)
print "User Name Sent"
#s.send(ConnectTo)  #removing to test
#print "Other User sent"
check = "true"
Incomming = s.recv(1024)
print Incomming 
print check
if Incomming == check:
  outgoing = "Client Entered Server Portion of Code"
  print outgoing
  s.send(outgoing)
  Port = s.recv(1024)
  Port = int(Port)
  print Port
  s.close()
  
  ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ServerS.bind((Address, Port))
  a = 0 
  ServerS.listen(5)
  while (a < 1):
  	Client, ClientAddr = ServerS.accept()
  	print "Got Connection from", ClientAddr
  	x = "Connected to: " + Address
  	Client.send(x)
  	ServerS.close()
  	a = a + 1
else:
  outgoing = "Client Entered Client Portion of Code"
  print outgoing
  s.send(outgoing)
  ServerAddr = s.recv(1024)
  print ServerAddr
  s.send(outgoing)
  Port = s.recv(1024)
  Port = int(Port)
  print Port
  s.close()
  
  cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  cs.connect((ServerAddr, Port)) # Make sure to check Firewall
  print "Socket Created"
  Incomming = cs.recv(1024)
  print Incomming
  cs.close()
print "All sockets Closed"
