#!/usr/bin/env python
import os
import socket
import pickle
import sys
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

# global Variables
i = 0
listlength = 5
nextopenspot = 0
logfile = ""

# gets the local IP address of the server
def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	Address = (s.getsockname()[0])
	s.close()
	return Address
	# end get_local_ip()

# check for zeus directory, create it if it doesnt exist
def check_log_dir():
	global logfile
	if not os.path.exists(os.path.expanduser('~') + '/.zeus'):
		print 'zeus not found, creating directory\n'
		os.makedirs(os.path.expanduser('~') + '/.zeus')
		print 'Directory created\n'
	return
	# done check_log_dir()

# Checks for the RSA key and returns whether it already exists or not
def check_key():
	global logfile
	logfile.write('Checking For Key\n')
	serverkeypath = os.path.expanduser('~') + '/.zeus/server.key'
	keyfound = True
	if not os.path.exists(serverkeypath):
		logfile.write('Server Key Not Found\n')
		keyfound = False
	else:
		logfile.write('Found Server Key\n')
	return keyfound
	# end check_key()

# checks to see if client key exists, if it doesn't then write it
def check_client_key(ClientA, exportedkey):
	global logfile
	keypath = os.path.expanduser('~') + '/.zeus/' + ClientA + '.pub'
	keyfound = True
	if not os.path.exists(keypath):
		print "in check client key"
		logfile.write('Public Key Not Found\n')
		dumpfile = open(keypath, 'a+')
		logfile.write('Public Key Added for: ')
		logfile.write(ClientA)
		logfile.write('\n')
		dumpfile.write(exportedkey)
		dumpfile.close()
	return
	# end check_client_key()

# if key does not exist it is created
def create_key(ServerPass):
	serverkeypath = os.path.expanduser('~') + '/.zeus/server.key'
	dumpfile = open(serverkeypath, 'w')
	key = RSA.generate(2048)
	server_key = key.exportKey('PEM', passphrase=ServerPass, pkcs=1) 
	dumpfile.write(server_key)
	dumpfile.close
	return
	# end create_key()

# loads the server private key
def load_key(ServerPass):
	serverkeypath = os.path.expanduser('~') + '/.zeus/server.key'
	loadfile = open(serverkeypath, 'a+')
	serverkey = loadfile.read()
	key = RSA.importKey(serverkey, ServerPass)
	loadfile.close()
	return key
	# end load_key()

# loads the client public key
def load_client_key(ClientA):
	keypath = os.path.expanduser('~') + '/.zeus/' + ClientA + '.pub'
	loadfile = open(keypath, 'a+')
	clientkey = loadfile.read()
	key = RSA.importKey(clientkey)
	loadfile.close()
	return key
	# end load_client_key()
	
# creates the server socket and leaves it in the listening state
def create_server_connection():
	global logfile
	logfile.write('Creating Server Socket\n')
	ServerS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logfile.write('Socket built succesfully\n')
	Port = 5000
	Address = get_local_ip()
	ServerS.bind((Address, Port))
	ServerS.listen(5)
	return ServerS
	# done create_server_connection():

# Searches the list for the username
def search_list(mylist, namea, nameb):
	global logfile, listlength, i, nextopenspot
	flag = False
	x = 0
	while x < listlength:
		if namea == mylist[x][1]:
			if nameb == mylist[x][0]:
				flag = True
				i = x
				logfile.write(namea)
				logfile.write(' found in list with ')
				logfile.write(nameb)
				logfile.write('\n')
		x = x + 1
	return flag
	# done search_list()

# find next empty spot in list
def find_next_open(mylist):
	x = 0 
	flag = True
	while x < listlength and flag == True:
		if mylist[x][0] == '*':
			nextopenspot = x
			flag = False
		x = x + 1
	return
	# done find_next_open()

# this function creates the session for the users and calls most other functions
def client_exchange(sessionlist, ServerS, ServerPass):
	global logfile, i
	if not check_key():
		print "going to create_key"
		create_key(ServerPass)
	serverkey = load_key(ServerPass)
	#Accept a client
	print "Waiting for Connection\n"
	Client, ClientAddr = ServerS.accept()
	logfile.write("\nConnected to: ")
	logfile.write(repr(ClientAddr))
	logfile.write("\n")
	pubkey = serverkey.publickey().exportKey()
	Client.send(pubkey)
	#getting info from Client
	#order is UserA, UserB, ClientIP
	recvdata = ["" for x in range(3)]
	recv_data_tmp = Client.recv(4096)
	Client.send("1738")
	recvkey = Client.recv(4096)
	recvdata= pickle.loads(serverkey.decrypt(pickle.loads(recv_data_tmp)))
	#print '\n', recvkey, '\n'
	print "Received Key From " + recvdata[0]
	check_client_key(recvdata[0], recvkey)
	clientkey = load_client_key(recvdata[0])
	#pass client name and sessionlist to search. 
	#return False if not in list
	#return True if in list
	check = search_list(sessionlist, recvdata[0], recvdata[1])
	#if client is in connection list
	#send False for server, ip to connect on, port to connect to, iv, key
	if (check == True):
		#info to be sent to client
		#| False for server | ip to connect to | port | iv | key |		
		outdata = ["" for x in range(5)]
		outdata[0] = False
		outdata[1] = sessionlist[i][2]
		outdata[2] = sessionlist[i][3]
		outdata[3] = sessionlist[i][4]
		outdata[4] = sessionlist[i][5]
#		out_data = clientkey.encrypt(pickle.dumps(outdata),32)
		Client.send(pickle.dumps(clientkey.encrypt(pickle.dumps(outdata),32)))
		sessionlist[i][0] = "*"
		sessionlist[i][1] = "*"
		sessionlist[i][2] = "*"
		sessionlist[i][3] = "*"
		sessionlist[i][4] = "*"
		sessionlist[i][5] = "*"
		logfile.write(str(sessionlist))
		#remove from list b/c session was created
	#if client is not in connection list
	#send True for server, port, iv, key
	if (check == False):
		find_next_open(sessionlist)
		#add to list in sessionlist[nextopenspot][0...]
		sessionlist[nextopenspot][0] = recvdata[0]
		sessionlist[nextopenspot][1] = recvdata[1]
		sessionlist[nextopenspot][2] = recvdata[2]
		sessionlist[nextopenspot][3] = 5005 + i
		sessionlist[nextopenspot][4] = Random.new().read(16)
		sessionlist[nextopenspot][5] = Random.new().read(16)
		logfile.write(str(sessionlist))
		#info to be sent to client
		#| True for server | filler | port | iv | key |
		outdata = ["" for x in range(5)]
		outdata[0] = True
		outdata[1] = "filler"
		outdata[2] = sessionlist[nextopenspot][3]
		outdata[3] = sessionlist[nextopenspot][4]
		outdata[4] = sessionlist[nextopenspot][5]
		Client.send(pickle.dumps(clientkey.encrypt(pickle.dumps(outdata),32)))
	Client.close()
	return sessionlist
	#done client_excange()

##############################################
#                                            #
#       Start Main, calling functions        #
#                                            #
##############################################

def main():
	global listlength, logfile
	print "Enter Password for Key: "
	ServerPass = raw_input()
	check_log_dir()
	logfile = open(os.path.expanduser('~') + '/.zeus/connection.log', 'a+')
	logfile.write("***File Opened***\n")
	# | ClientA(server) | ClientB(Client) | ClientAIP | Port | IV | Key
	sessionlist = [["*" for x in range(6)] for x in range(listlength)]

	#Start Program
	ServerS = create_server_connection()
	while True:
		sessionlist = client_exchange(sessionlist, ServerS, ServerPass)
		#done while
	logfile.write("***Closeing File***\n")
	logfile.close()
	#done main()

if __name__ == '__main__':
	main()
