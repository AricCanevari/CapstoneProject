Goal:

Instructions:

To be able to use our project, you will need some prerequisites. The first is the operating system. Because of the way sockets are handled and used, a Unix like operating system will need to be used. We have successfully used our project on the Computer Science department’s “fang” server, on Ubuntu 14.04.1 and on Mac with some extra configuration. Ultimately, any distribution should work as long as you are able to get the other prerequisites. The next will be python 2.7. We chose python as our language for our program because of its portability. Unfortunately, because of how sockets are handled in windows vs python, we decided to fixate on the Unix like operating systems, so the interoperability was not useful for our project. The last two prerequisite are pycrypto and git. This is a library that may not come with the normal packages included in python 2.7. Because of this you may need to install it separately. On mac you will need to install xcode to get pycrypto, while Ubuntu it works easily with the following command: “apt-get install python-crypto”. Git will be used to install and update our program. “Git clone https://github.com/ canevaa/CapstoneProject.git“ will be used to download the programs. “git pull in the directory will update it if there are any updates. Also, due to the point to point connection and NAT problem (covered in future works), the clients will be required to be on the same network. Otherwise they will not be able to connect to each other.  

After the prerequisites and the install, you are ready to start the program. First we will start with the server. We have a dedicated computer at Louie’s house which will act as our server. We port forwarded port 5000 to this server so it can receive connections from the internet. We will start running the server script by typing “python Server-5000.py” into the terminal in the “CapstonProject” directory. It will create the ~/.zeus directory which will hold all of our keys and log files. The server script will ask you to create a password for the server key, or ask you to enter the key if it has already been created. 

With the server started and waiting for connections, we will move to ClientA. ClientA will install the program the same way and start the client code by entering “python Client-5000.py” into the terminal in the “CapstoneProject” directory. The program will ask for the current clients user name, which will be “ClientA”, and the user name of the client to connect to, which will be “ClientB”. If a key and password has not been created it will ask the user to create a password, and it will also ask the user to accept the server key. This is an important point of trust, just like OpenSSH has. Client B goes through the same steps on their side and after the connection they should be able to communicate freely. For screenshots please refer to the Results section. 

Future Works:




