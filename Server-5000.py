#!/usr/bin/python
import socket
import subprocess

#Gets the local IP address of server and returns it
def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	Address = (s.getsockname()[0])
	s.close()
	return Address
	
#Creates the Server Socket for messaging returns server socket
def create_server_connection():
	ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Port = 5000
	ServerS.bind((Address, Port))
	ServerS.listen(5)
	return ServerS

#Takes connections from the clients then connects them to each other
def connect_with_clients():
	clientport = "5005"
	a = 0
	while (a < 2):
		Client, ClientAddr = ServerS.accept()
		print "Got Connection from", ClientAddr
		x = "Connected to Server"
		Client.send(x)
		ClientIP = Client.recv(1024)
		print "ClientIP recv"
		ClientUN = Client.recv(1024)
		print "ClientUN recv"
#		ClientCT = Client.recv(1024) #Code is freezing here? why?? removing to test
#		print "ClientCT recv"
		if (a == 0):
			print "Entered if a = 0"
			outgoing = "true"
			Client.send(outgoing)
			print Client.recv(1024)
			Client.send(clientport)
			ClientAIP = ClientIP
		if (a == 1):
			print "Entered if a = 1"
			outgoing = "false"
			Client.send(outgoing)
			print Client.recv(1024)
			Client.send(ClientAIP)
			print Client.recv(1024)
			Client.send(clientport)
		Client.close()
		a=a+1
	ServerS.close()
	
#------------------------------------------------------------
	
Address = get_local_ip()
ServerS = create_server_connection()
connect_with_clients()

#Creates a connection to get public address of itself
#Address = subprocess.check_output("wget http://people.sunyit.edu/~greenli/ip.php -qO -", shell=True)
