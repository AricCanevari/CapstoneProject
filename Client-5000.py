#!/usr/bin/python
import socket
import subprocess

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	Address = (s.getsockname()[0])
	s.close()
	return Address
	
def get_user_input():
	Prompt = '>'
	print "Enter User Name"
	UserName = raw_input(Prompt)
	print "Connect to?"
	ConnectTo = raw_input(Prompt)
	return(UserName, ConnectTo)
	
def connect_to_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ServerAddr = "67.241.38.178"
	Port = 5000
	s.connect((ServerAddr, Port))
	return(s)

#-------------------------------------------------------------------
#        	Start Calling Functions for use!
#-------------------------------------------------------------------


Address = get_local_ip()
UserName, ConnectTo = get_user_input()
s = connect_to_server()



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
  	print "Creating Socket"
  	ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  	ServerS.bind((Address, Port))
  	print "Socket created, waiting for connection:"
  	ServerS.listen(5)
  	Client, ClientAddr = ServerS.accept()
  	print "Got Connection from", ClientAddr
  	x = "Connected to: " + Address
  	Client.send(x)
  	ServerS.close()
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


#Gets client external address
#Address = subprocess.check_output("wget http://people.sunyit.edu/~greenli/ip.php -qO -", shell=True)
