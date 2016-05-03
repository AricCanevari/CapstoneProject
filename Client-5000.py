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
from Crypto.Hash import MD5

#Global variables
logfile = ""
ClientA = ""
ClientB = ""
Client = ""
CS = ""
cipher1 = ""
cipher2 = ""
quit = False

# Gets the local IP Address of the computer
def get_local_ip():
 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 	s.connect(("gmail.com",80))
 	Address = (s.getsockname()[0])
 	Address = str(Address)
 	s.close()
 	return Address
 	# end get_local_address

# check for hermes directory, create it if it doesnt exist
def check_log_dir():
	hermespath = os.path.expanduser('~') + '/.hermes'
	if not os.path.exists(hermespath):
		print '~/.hermes not found, creating directory\n'
		os.makedirs(hermespath)
	return
	# done check_log_dir()

# Checks for the RSA key and returns whether it already exists or not
def check_key():
	global logfile, ClientA
	logfile.write('Checking For Key\n')
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	pubkeypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.pubkey'
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
	if not os.path.exists(pubkeypath):
		logfile.write('Full Key Not Found\n')
		filekey = open(pubkeypath, 'a+')
		keyfound = False
	else:
		logfile.write('Found Full Key\n')
	if not os.path.exists(serverkeypath):
		logfile.write('Server Key Not Found\n')
		filekey = open(serverkeypath, 'a+')
		keyfound = False
	else:
		logfile.write('Found Server Key\n')
	return keyfound
	# done check_key()

# Creates the client key with a password and writes the server public key to a file
def create_key(server_key, s):
	global ClientA
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	pubkeypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.pubkey'
	serverkeypath = os.path.expanduser('~') + '/.hermes/server.pub'
	# Creates and writes client key
	print "New Password For Key: "
	password = raw_input()
	key = RSA.generate(2048)
	export_key = key.exportKey('PEM', password, pkcs=1)
	dumpfile = open(keypath, 'w')
	dumpfile.write(export_key)
	dumpfile.close
	# Writes the pubkey to a file
	pubkey = key.publickey().exportKey()
	dumpfile = open(pubkeypath, 'w')
	dumpfile.write(pubkey)
	dumpfile.close
	# Writes server key public ket to file
	print "The following Server Public Key will be created: \n"
	print server_key, "\n"
	print "Please Type 'Yes' to accept this key: "
	flag = raw_input()
	if flag == 'Yes':
		dumpfile = open(serverkeypath, 'w')
		dumpfile.write(server_key)
		dumpfile.close
#causes server to close, not that good of a solution
	else:
	#	os.remove(serverkeypath) #I dont think we need this because it should not write to the file if it says no. 
					 #If another user is using the key, it breaks it. 
		print "Key not accepted."
		logfile.write("You did not accept the key.\n")
		s.close()
		logfile.write("Socket to server closed.\n")
		logfile.close()
		sys.exit(1)
	return pubkey
	# end create_key()

# Loads the key into a variable for use with the proper password
def load_key():
	global ClientA
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.key'
	importfile = open(keypath, 'r')
	print "Password For " + ClientA + " Key: "
	password = raw_input()
	key = RSA.importKey(importfile.read(), passphrase=password)
	importfile.close()
	return key
	# end load_key()

# Loads the pubkey into a variable
def load_pub_key():
	global ClientA
	keypath = os.path.expanduser('~') + '/.hermes/' + ClientA + '.pubkey'
	importfile = open(keypath, 'r')
	key = importfile.read()
	importfile.close()
	return key
	
# Loads the server key into a variable for use
def load_server_key(passed_key):
	serverkeypath = os.path.expanduser('~') + '/.hermes/server.pub'
	importfile = open(serverkeypath, 'r')
	key = importfile.read()
	if passed_key == key:
		key = RSA.importKey(key)
	else:
		print "Error: Server Key does not match! Possible Man in the Middle!"
	importfile.close()
	return key
	# end load_server_key()

# Creates a socket and connects to the other computer who became the server
def client_socket(Server_Address, Server_Port):
	global logfile 
	logfile.write('Creating Client Socket\n')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logfile.write('Client Socket Created\n')
	logfile.write('Connecting to Server\n')
	s.connect((Server_Address, Server_Port))
	logfile.write('Connection Created\n')
	return s
	# end create_socket()

# Creates a socket and waits for the other computer to connect
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
	# end server_socket()
	
# Used from the threading statment. It will continuously wait for a message
def recv_thread(mssg):
	global ClientB, ClientA, CS, Client, cipher1, cipher2, quit
	data_enc = ""
	data_unenc = ""
	prompt = "[" + ClientA + "]: "
	if (mssg == 1):
		while quit == False:
			data_enc = Client.recv(1024)
			data_unenc = cipher2.decrypt(data_enc)
			if (data_unenc == "quit()"):
				quit = True
				break
			sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
			#print "[" + ClientB + " Encrypted]: " + data_enc
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
			sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
			#print "[" + ClientB + " Encrypted]: " + data_enc
			print "[" + ClientB + "]: " + data_unenc
			sys.stdout.write(prompt + readline.get_line_buffer())
			sys.stdout.flush()
	# end recv_thread()

# Used from the threading statment. It will send whenever it gets a message
def send_thread(mssg):
	global ClientA, CS, ServerS, cipher1, cipher2, quit
	data = ""
	prompt = "[" + ClientA + "]: "
	if (mssg == 1):
		while quit == False:
			data = raw_input(prompt)
			Client.send(cipher1.encrypt(data))
			if (data == "quit()"):
				quit = True
	if (mssg == 2):
		while quit == False:
			data = raw_input(prompt)
			CS.send(cipher2.encrypt(data))
			if (data == "quit()"):
				quit = True
	# end send_thread()

# Handles the Server Portion of the messanger 
# | Server | ip | port | IV | Key | 
def mess_server(sessionlist):
	global logfile, Client
	ServerS = server_socket(sessionlist[2])
	print "Waiting for Connection\n"
	Client, ClientAddr = ServerS.accept()
	logfile.write("Connected to: ")
	logfile.write(repr(ClientAddr))
	logfile.write("\n")
	# Create threads for sending and recv messages
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
	# end mess_server()

# Handles the Client Portion of the messanger
# | Server | ip | port | IV | Key | 	
def mess_client(sessionlist):
	global logfile, CS
	CS = client_socket(sessionlist[1], sessionlist[2])
	print CS.recv(1024)
	# Create threads for sending and recv messages
	t1 = Thread(target=recv_thread, args=(2,))
	t2 = Thread(target=send_thread, args=(2,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	CS.close()
	logfile.write("All sockets Closed\n")
	# end mess_client()

# Exchange between server and clients
def server_exchange(ServerAddr):
	global logfile, ClientA, ClientB, cipher1, cipher2
	# order is UserA, UserB, ClientIP
	senddata = ["" for x in range(3)]
	print "Enter Your User Name:"
	senddata[0] = raw_input('>')
	ClientA = senddata[0]
	print "Enter User to Connect To:"
	senddata[1] = raw_input('>')
	ClientB = senddata[1]
	senddata[2] = get_local_ip()
	# Creating socket to Server
	s = client_socket(ServerAddr, 5000)
	# recv server_pub_key
	server_pub_key = s.recv(4096)
	if not check_key():
		send_data_tmp2 = create_key(server_pub_key, s)
	# Loading private key to variable
	key = load_key()
	# Loading server public key to variable
	serverkey = load_server_key(server_pub_key)
	send_data_tmp2 = load_pub_key()
	# Sending array with connection info
	s.send(pickle.dumps(serverkey.encrypt(pickle.dumps(senddata))))
	# ACK from server
	tmp = s.recv(1024)
	# Sending our public key
	s.send(send_data_tmp2)
	# | Server | ip | port | IV | Key |
	recvdata = ["" for x in range(5)]
	recv_data_tmp = s.recv(4096) 
	recvdata = pickle.loads(key.decrypt(pickle.loads(recv_data_tmp)))
	# creating ciphers
	cipher1 = AES.new(recvdata[4], AES.MODE_CFB, recvdata[3])
	#hashing they key and iv so the second cipher is different and cannot be decrypted
	hashkey = MD5.new(recvdata[4]).digest()
	hashiv = MD5.new(recvdata[3]).digest()
	cipher2 = AES.new(hashkey, AES.MODE_CFB, hashiv)
	# if recvdata[0] true: mess_server() else: mess_client()
	logfile.write(str(recvdata))
	logfile.write("\n")
	if recvdata[0] == True:
		mess_server(recvdata)
	if recvdata[0] == False:
		mess_client(recvdata)
	s.close()
	# end server_exchange()

##############################################
#                                            #
#       Start Main, calling functions        #
#                                            #
##############################################

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
