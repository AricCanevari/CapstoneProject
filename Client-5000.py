#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
Address = (s.getsockname()[0])
s.close()

print "Enter User Name"
Prompt = '>'
UserName = raw_input(Prompt)

print "Connect to?"
ConnectTo = raw_input(Prompt)

s = socket.socket()
ServerAddr = "67.241.38.178" 
Port = 5000

s.connect((ServerAddr, Port))
Incomming = s.recv(1024)
print Incomming
s.send(Address)
s.send(UserName)
s.send(ConnectTo)
Incomming = s.recv(1024)
if (Incomming == "true"):
  Port = s.recv(1024)
  s.close()
  ServerS = socket.socket()
  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com",80))
  Address = (s.getsockname()[0])
  s.close()

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
if (Incomming == "false"):
  ServerAddr = s.recv(1024)
  Port = s.recv
  s.close()
  s = socket.socket()
 
  s.connect((ServerAddr, Port))
  Incomming = s.recv(1024)
  print Incomming
  s.close()
print "All sockets Closed"
