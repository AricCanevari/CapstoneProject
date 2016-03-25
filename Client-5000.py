#!/usr/bin/python
import socket
import subprocess
import threading


def get_local_ip():
 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 	s.connect(("gmail.com",80))
 	Address = (s.getsockname()[0])
 	Address = str(Address)
 	print Address
 	s.close()
#Gets user input for connections and returns it
def get_user_input():
	Prompt = '>'
	print "DDNS Host Name"
	UserName = raw_input(Prompt)
	UserName = str(UserName)
	print UserName
	print "Connect to?"
	ConnectTo = raw_input(Prompt)
	return(UserName, ConnectTo)

def recvthread(mssg):
	print mssg
	if (mssg == 1):
		quit = False
		while quit == False:
			data = Client.recv(size)
			print "\r[Other]:" + data
			if (data == "quit\n"):
				quit = True
	if (mssg == 2):
		quit = False
		while True:
			data = cs.recv(size)
			print "\r[Other]:" + data
			if (data == "quit\n"):
				quit = True

def sendthread(mssg):
	print mssg
	if (mssg == 1):
		while True:
			data = raw_input()
			print "[Me]>" + data
			Client.send(data)
	if (mssg == 2):
		while True:
			data = raw_input()
			print "[Me]>" + data
			cs.send(data)

#sets up the connection with the server and returns client information
def connect_to_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ServerAddr = "67.241.38.178"
	Port = 5000
	s.connect((ServerAddr, Port))
	check = "true"
	Incomming = s.recv(1024)
	print Incomming
	#s.send(Address)
	#print "Address sent: " + Address
	s.send(UserName)
	print "User Name Sent: " + UserName
	#s.send(ConnectTo)  #removing to test
	#print "Other User sent"
	Incomming = s.recv(1024)
	if(Incomming == check):
		outgoing = "Client Entered Server Portion of Code"
		print outgoing
		s.send(outgoing)
		Port = s.recv(1024)
		Port = int(Port)
		print Port
		s.close()
		Server_Code(Port)
	else:
		outgoing = "Client Entered Client Portion of Code"
  		print outgoing
		s.send(outgoing)
		ServerAddr = s.recv(1024)
		print ServerAddr
		s.send(outgoing)
		Port = s.recv(1024)
		Port = int(Port)
		s.close()
		print "Closed connection to Server"
		Client_Code(ServerAddr, Port)
	return
		

def Server_Code(Port):
	print "Creating Server Socket"
	ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ServerS.bind((Address, Port))
	print "Server Socket created, waiting for connection:"
	ServerS.listen(5)
	Client, ClientAddr = ServerS.accept()
	print "Got Connection from", ClientAddr
	x = "Connected to: " + Address
	Client.send(x)
	
	################################
	#####Server Messaging Part:#####
	################################
	t1 = Thread(target=recvthread, args=(1,))
	t2 = Thread(target=sendthread, args=(1,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
	ServerS.close()
	print "end of server portion"
	return
	
	
def Client_Code(ServerAddr, Port):
	print "Connecting to Other Client"
	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cs.connect((ServerAddr, Port)) # Make sure to check Firewall
	print "Socket Created"
	Incomming = cs.recv(1024)
	print Incomming
	
	################################
	#####Client Messaging Part:#####
	################################
	t1 = Thread(target=recvthread, args=(2,))
	t2 = Thread(target=sendthread, args=(2,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
	
	print "All sockets Closed"
	cs.close()
	return

#-------------------------------------------------------------------
#        	Start Calling Functions for use!
#-------------------------------------------------------------------

Address = get_local_ip()
UserName, ConnectTo = get_user_input()
SendAddress = UserName
connect_to_server()

#Gets client external address
#Address = subprocess.check_output("wget http://people.sunyit.edu/~greenli/ip.php -qO -", shell=True)
