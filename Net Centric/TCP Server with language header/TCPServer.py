#TCPServer.py

import os
import time
from socket import socket, SOCK_STREAM, AF_INET
#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort=1717
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "Interrupt with CTRL-C"
while True:
	try:
		connectionSocket, addr = serverSocket.accept()
		print "Connection from %s port %s" % addr
		# Receive the client packet
		message = connectionSocket.recv(2048)
                print "Orignal message from client: ", message
		# Capitalize the message from the client
		
		filename = ""
		
		if message != "":
			filename = message.split()[1].partition("/")[2]
		
		languageHeader = message.find("Accept-Language:", 0, len(message))
		languagePartition = message[languageHeader: len(message)].split('\n')[0]
		if languagePartition != "":
			language = languagePartition.split()[1].split(",")
		
			for lan in language:
				if lan.find("en") != -1:
					extension = '.en'
				elif lan.find("es") != -1:
					extension = '.es'
				elif lan.find("fr") != -1:
					extension = '.fr'
				elif lan.find("de") != -1:
					extension = '.de'
			
		if os.path.isfile(filename):
			lastMod = time.ctime(os.path.getmtime(filename))
		
			parsedData = {}
			ifMod = filename.split('\r\n')
			for mod in ifMod:
				if 'If-Modified-Since' in mod:
					modList = mod.split(': ', 1)
					name = modlist[0]
					value = modList[1]
					parsedData[name] = value
				else:
					name = 'If-Modified-Since'
					value = 'Nothing'
					parsedData[name] = value
			
			file = open(filename, 'rU').read()
		
			if parsedData['If-Modified-Since'] == lastMod:
				print("Up to date")
				connectionSocket.send('HTTP/1.1 304 Not Modified\n\n')
			else:
				print("Resending")
				size = os.path.getsize(filename)
				connectionSocket.send('HTTP/1.1 200 OK\n')
				connectionSocket.send("Last-Modified: %s\n" % lastMod)
				connectionSocket.send("Content-Length: %d\n" % size)
				connectionSocket.send('Content-type: text/html\n')
				connectionSocket.send('Accept-Language: en, es, fr, de\n\n')
				connectionSocket.send('\n')
				connectionSocket.send(file)
				connectionSocket.close()
	
	except IOError:
		
		file = open('error.html', 'r')
		message = file.read()
		print "404 Not Found"
		connectionSocket.send('\HTTP/1.1 404 Not Found\n')
		connectionSocket.send('Content-type: text/html\n\n')
		connectionSocket.send(message)
		connectionSocket.close()
	except KeyboardInterrupt:
		print "\nInterrupted by CTRL-C"
		break
serverSocket.close()
