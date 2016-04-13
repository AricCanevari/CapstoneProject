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
Client = ""
CS = ""
cipher1 = ""
cipher2 = ""

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
	Address = get_local_ip()
	ServerS.bind((Address, Port))
	logfile.write('Waiting for a Connection\n')
	ServerS.listen(5)
	return ServerS
	
#Used from the threading statment. It will continuously wait for a message
def recv_thread(mssg):
	global ClientB, CS, Client, cipher1
	quit = False
	data = ""
	print mssg
	if (mssg == 1):
		while quit == False:
			if (cipher2.decrypt(data) == "quit"):
				quit = True #not working, Why??
				CS.close()
			data = Client.recv(1024)
			print "Encrypted: " + data
			print "\r[" + ClientB + "]: " + cipher2.decrypt(data)
			
	if (mssg == 2):
		while True:
			if (cipher2.decrypt(data) == "quit"):
				quit = True
				CS.close()
			data = CS.recv(1024)
			print "Encrypted: " + data
			print "\r[" + ClientB + "]: " + cipher2.decrypt(data)
	#end recv_thread()

#Used from the threading statment. It will send whenever it gets a message
def send_thread(mssg):
	global ClientA, CS, ServerS, cipher2
	quit = False
	data = ""
	print mssg
	if (mssg == 1):
		while quit == False:
			data = raw_input()
			print "[" + ClientA + "]> " + data
			Client.send(cipher1.encrypt(data))
			if (data == "quit"):
				quit = True
				CS.close()
	if (mssg == 2):
		while quit == False:
			data = raw_input()
			print "[" + ClientA + "]> " + data
			CS.send(cipher1.encrypt(data))
			if (data == "quit"):
				quit = True
				CS.close()
	#end send_thread()

#Handles the Server Portion of the messanger 
# | Server | ip | port | IV | Key | 
def mess_server(sessionlist):
	global logfile, Client
	ServerS = server_socket(sessionlist[2])
	Client, ClientAddr = ServerS.accept()
	logfile.write("Connected to: ")
	logfile.write(repr(ClientAddr))
	logfile.write("\n")
	#Create threads for sending and recv messages
	Client.send("Connection Established")
	print "Connection Established"
	logfile.write("Starting Threads\n")
	t1 = Thread(target=recv_thread, args=(1,))
	t2 = Thread(target=send_thread, args=(1,))
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
	global logfile, CS
	CS = client_socket(sessionlist[1], sessionlist[2])
	print CS.recv(1024)
	#Create threads for sending and recv messages
	t1 = Thread(target=recv_thread, args=(2,))
	t2 = Thread(target=send_thread, args=(2,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	cs.close()
	logfile.write("All sockets Closed\n")
	#end mess_client()

def server_exchange(ServerAddr):
	global logfile, ClientA, ClientB, cipher1, cipher2
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
	s = client_socket(ServerAddr, 5000)
	s.send(str(send_data_tmp))
	recvdata = ["" for x in range(5)]
	recv_data_tmp = s.recv(2048)
	# | Server | ip | port | IV | Key | 
	recvdata = pickle.loads(recv_data_tmp)
	#creating ciphers
	cipher1 = AES.new(recvdata[4], AES.MODE_CFB, recvdata[4])
	cipher2 = AES.new(recvdata[4], AES.MODE_CFB, recvdata[4])
	#if recvdata[0] true: mess_server() else: mess_client()
	logfile.write(str(recvdata))
	logfile.write("\n")
	if recvdata[0] == True:
		mess_server(recvdata)
	if recvdata[0] == False:
		mess_client(recvdata)
	s.close()
	#end server_exchange()

def main():
	global logfile
	check_log_dir()
	logfile = open('/var/log/hermes/connection.log', 'a+')
	logfile.write("***File Opened***\n")
	ServerAddr = "67.241.38.178" 
	server_exchange(ServerAddr)
	#end main()


if __name__ == '__main__':
	main()
