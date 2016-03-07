#!/usr/bin/python
#Test from Louie
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
  int(Port)
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
  print "Entered Client Portion of Code"
  ServerAddr = s.recv(1024)
  Port = s.recv
  s.close()
  cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
  cs.connect((ServerAddr, Port))
  Incomming = cs.recv(1024)
  print Incomming
  cs.close()
print "All sockets Closed"
