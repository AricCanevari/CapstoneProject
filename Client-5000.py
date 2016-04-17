#!/usr/bin/python
import os
import socket
import subprocess
import pickle
import time
import readline
import sys
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
quit = False

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
	hermespath = os.path.expanduser('~') + '/.hermes'
	if not os.path.exists(hermespath):
		print '~/.hermes not found, creating directory\n'
		os.makedirs(hermespath)
	#done check_log_dir()

def check_key():
	global logfile, ClientA
	logfile.write('Checking For Key\n')
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	serverkeypath = os.path.expanduser('~') + '/.hermes/server.pub'
	logfile.write('Full Key Path: ')
	logfile.write(keypath)
	logfile.write('\n')
	logfile.write('Server Key Path: ')
	logfile.write(serverkeypath)
	logfile.write('\n')
	keyfound = True
	if not os.path.exists(keypath):
		logfile.write('Full Key Not Found\n')
		filekey = open(keypath, 'a+')
		keyfound = False
	else:
		logfile.write('Found Full Key\n')
	if not os.path.exists(serverkeypath):
		logfile.write('Server Key Not Found\n')
		filekey = open(keypath, 'a+')
		keyfound = False
	else:
		logfile.write('Found Server Key\n')
	return keyfound
	#done check_key()
	
def create_key(server_key):
	global ClientA
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	serverkeypath = os.path.expanduser('~') + '/.hermes/server.pub'
	print "New Password For Key: "
	password = raw_input()
	key = RSA.generate(2048)
	export_key = key.exportKey('PEM', password, pkcs=1)
	dumpfile = open(keypath, 'w')
	dumpfile.write(export_key)
	dumpfile.close
	dumpfile = open(serverkeypath, 'w')
	dumpfile.write(server_key)
	dumpfile.close
	
	#end create_key()
	
def load_key():
	global ClientA
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	importfile = open(keypath, 'r')
	print "Password For " + ClientA + " Key: "
	password = raw_input()
	key = RSA.importKey(importfile.read(), passphrase=password)
	importfile.close()
	return key
	#end load_key()
	
def load_server_key():
	serverkeypath = os.path.expanduser('~') + '/.hermes/server.pub'
	importfile = open(serverkeypath, 'r')
	key = RSA.importKey(importfile.read())
	importfile.close()
	return key
	#end load_server_key()

def client_socket(Server_Address, Server_Port):
	global logfile 
	logfile.write('Creating Client Socket\n')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logfile.write('Client Socket Created\n')
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
	global ClientB, ClientA, CS, Client, cipher1, cipher2, quit
	data_enc = ""
	data_unenc = ""
	prompt = "[" + ClientA + "]: "
#	print mssg
	if (mssg == 1):
		while quit == False:
			data_enc = Client.recv(1024)
			data_unenc = cipher2.decrypt(data_enc)
			if (data_unenc == "quit()"):
				quit = True
				break
#			print "Encrypted: " + data_enc
			sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
			print "[" + ClientB + "]: " + data_unenc
			sys.stdout.write(prompt + readline.get_line_buffer())
			sys.stdout.flush()
			
	if (mssg == 2):
		while quit == False:
			data_enc = CS.recv(1024)
			data_unenc = cipher1.decrypt(data_enc)
			if (data_unenc == "quit()"):
				quit = True
				break
#			print "Encrypted: " + data_enc
			sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
			print "[" + ClientB + "]: " + data_unenc
			sys.stdout.write(prompt + readline.get_line_buffer())
			sys.stdout.flush()
	#end recv_thread()

#Used from the threading statment. It will send whenever it gets a message
def send_thread(mssg):
	global ClientA, CS, ServerS, cipher1, cipher2, quit
	data = ""
	prompt = "[" + ClientA + "]: "
#	print mssg
	if (mssg == 1):
		while quit == False:
			data = raw_input(prompt)
#			print "[" + ClientA + "]> " + data
			Client.send(cipher1.encrypt(data))
			if (data == "quit()"):
				quit = True
	if (mssg == 2):
		while quit == False:
			data = raw_input(prompt)
#			print "[" + ClientA + "]> " + data
			CS.send(cipher2.encrypt(data))
			if (data == "quit()"):
				quit = True
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
	CS.close()
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
	s = client_socket(ServerAddr, 5000)
	#recv server_pub_key
	server_pub_key = s.recv(4096)
	if not check_key():
		create_key(server_pub_key)
	key = load_key()
	serverkey = load_server_key()
	sendkey = key.publickey().exportKey()
	send_data_tmp = pickle.dumps(serverkey.encrypt(senddata, 32))
	send_data_tmp2 = pickle.dumps(serverkey.encrypt(sendkey, 32))
	s.send(str(send_data_tmp))
	s.send(str(send_data_tmp2))
	recvdata = ["" for x in range(5)]
	recv_data_tmp = s.recv(4096)
	# | Server | ip | port | IV | Key | 
	recvdata = key.decrypt(pickle.loads(recv_data_tmp))
	#creating ciphers
	cipher1 = AES.new(recvdata[4], AES.MODE_CFB, recvdata[3])
	cipher2 = AES.new(recvdata[4], AES.MODE_CFB, recvdata[3])
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
	logfile = open(os.path.expanduser('~') + '/.hermes/connection.log', 'a+')
	logfile.write("***File Opened***\n")
	ServerAddr = "67.241.38.178" 
	server_exchange(ServerAddr)
	logfile.write("***File Closed***\n")
	logfile.close()
	#end main()


if __name__ == '__main__':
	main()
