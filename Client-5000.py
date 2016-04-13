#!/usr/bin/python
import os
import socket
import subprocess
import pickle
from threading import Thread
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

#Open file for logging

logfile = ""
ClientA = ""
ClientB = ""

#Gets the local IP Address of the computer
def get_local_ip():
 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 	s.connect(("gmail.com",80))
 	Address = (s.getsockname()[0])
 	Address = str(Address)
 	s.close()
 	return Address
 	#End get_local_address

#check for hermes directory, create it if it doesnt exist
def check_log_dir():
	global logfile
	if not os.path.exists('/var/log/hermes'):
		print '/var/log/hermes not found, creating directory\n'
		os.makedirs('/var/log/hermes')
	#done check_log_dir()

def client_socket(Server_Address, Server_Port):
	global logfile 
	logfile.write('Createing Clinet Socket\n')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logfile.write('Clinet Socket Created\n')
	logfile.write('Connecting to Server\n')
	s.connect((Server_Address, Server_Port))
	logfile.write('Connection Created\n')
	return s
	#end create_socket()

def server_socket(Port):
	global logfile
	logfile.write('Creating Server Socket\n')
	ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logfile.write('Socket built succesfully\n')
	Port = 5000
	Address = get_local_ip()
	ServerS.bind((Address, Port))
	logfile.write('Waiting for a Connection\n')
	ServerS.listen(5)
	return ServerS
	
#Used from the threading statment. It will continuously wait for a message
def recv_thread(mssg, s):
	global ClientB
	quit = False
	data = ""
	print mssg
	if (mssg == 1):
		while quit == False:
			if (data == "quit"):
				quit = True #not working, Why??
			data = s.recv(1024)
			print "\r[", ClientB, "]: ", data
			
	if (mssg == 2):
		while True:
			if (data == "quit"):
				quit = True
			data = s.recv(1024)
			print "\r[", ClientB, "]: ", data
	#end recv_thread()

#Used from the threading statment. It will send whenever it gets a message
def send_thread(mssg, s):
	global ClientA
	quit = False
	data = ""
	print mssg
	if (mssg == 1):
		while quit == False:
			data = raw_input()
			print "[", ClientA, "]> ", data
			s.send(data)
			if (data == "quit"):
				quit = True
	if (mssg == 2):
		while quit == False:
			data = raw_input()
			print "[", ClientA, "]> ", data
			s.send(data)
			if (data == "quit"):
				quit = True
	#end send_thread()

#Handles the Server Portion of the messanger 
# | Server | ip | port | IV | Key | 
def mess_server(sessionlist):
	global logfile
	ServerS = server_socket(sessionlist[2])
	Client, ClientAddr = ServerS.accept()
	logfile.write("Connected to: ")
	logfile.write(repr(ClientAddr))
	logfile.write("\n")
	#Create threads for sending and recv messages
	logfile.write("Starting Threads\n")
	t1 = Thread(target=recvthread, args=(1,ServerS,))
	t2 = Thread(target=sendthread, args=(1,ServerS,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	ServerS.close()
	logfile.write("Server Socket Closed\n")
	#end mess_server()

#Handles the Client Portion of the messanger
# | Server | ip | port | IV | Key | 	
def mess_client(sessionlist):
	global logfile
	s = client_socket(sessionlist[1], sessionlist[2])
	t1 = Thread(target=recvthread, args=(2,s,))
	t2 = Thread(target=sendthread, args=(2,s,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	cs.close()
	logfile.write("All sockets Closed\n")
	#end mess_client()

def server_exchange(ServerAddr):
	global logfile, ClientA, ClientB
	s = client_socket(ServerAddr, 5000)
	#order is UserA, UserB, ClientIP
	senddata = ["" for x in range(3)]
	print "Enter Your User Name:"
	senddata[0] = raw_input('>')
	ClientA = senddata[0]
	print "Enter User to Connect To:"
	senddata[1] = raw_input('>')
	ClientB = senddata[1]
	senddata[2] = get_local_ip()
	send_data_tmp = pickle.dumps(senddata)
	s.send(str(send_data_tmp))
	recvdata = ["" for x in range(5)]
	recv_data_tmp = s.recv(2048)
	# | Server | ip | port | IV | Key | 
	recvdata = pickle.loads(recv_data_tmp)
	#if recvdata[0] true: mess_server() else: mess_client()
	if recvdata[0] == True:
		mess_server()
	if recvdata[0] == False:
		mess_client()
	s.close()
	#end server_exchange()

def main():
	global logfile
	check_log_dir()
	logfile = open('/var/log/hermes/connection.log', 'a+')
	logfile.write("***File Opened***\n")
	ServerAddr = "67.241.38.178" #"127.0.0.1"
	server_exchange(ServerAddr)
	#end main()


if __name__ == '__main__':
	main()
