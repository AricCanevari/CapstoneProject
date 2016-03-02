#!/usr/bin/python
import socket

ServerS = socket.socket()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
Address = (s.getsockname()[0])
s.close()

Port = 5000
ServerS.bind((Address, Port))
a = 0 
clientport = "5005"

ServerS.listen(5)
while (a < 2):
	Client, ClientAddr = ServerS.accept()
	print "Got Connection from", ClientAddr
	x = "Connected to: " + Address
	Client.send(x)
	ClientIP = Client.recv(1024)
	ClientUN = Client.recv(1024)
	ClientCT = Client.recv(1024)
	if (a == 0):
		Client.send("true")
		Client.send(clientport)
	if (a == 1):
		Client.send("false")
		Client.send(ClientAIP)
		Client.send(clientport)
	Client.close()
	a=a+1
	
ServerS.close()

