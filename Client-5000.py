#!/usr/bin/python
import os
import socket
import subprocess
import pickle
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

#Open file for logging

logfile = ""

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

def server_exchange(ServerAddr):
	global logfile
	s = client_socket(ServerAddr, 5000)
	#order is UserA, UserB, ClientIP
	senddata = ["" for x in range(3)]
	print "Enter Your User Name:"
	senddata[0] = raw_input('>')
	print "Enter User to Connect To:"
	senddata[1] = raw_input('>')
	senddata[2] = get_local_ip()
	send_data_tmp = pickle.dumps(senddata)
	s.send(str(send_data_tmp))
	recvdata = ["" for x in range(5)]
	recv_data_tmp = s.recv(2048)
	# | Server | ip | port | IV | Key | 
	recvdata = pickle.loads(recv_data_tmp)
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
