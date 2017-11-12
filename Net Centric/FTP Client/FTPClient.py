#FTPClient.py
#!/usr/bin/python

import os, codecs
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
import socket
import time
import re
import binascii

from ast import literal_eval

def send(socket, msg):
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	recv = socket.recv(1024)
	print "<=== receive: " + recv
	return recv

serverName = 'ftp.swfwmd.state.fl.us'
serverPort = 21
clientSocket = socket.socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
condition220 = True
message = clientSocket.recv(2048)
print message

while condition220:
	message = clientSocket.recv(2048)
	print message
	condition220 = message[0:6] != "220---"
message = send(clientSocket,"USER Anonymous")
message = send(clientSocket,"PASS bbast005@fiu.edu")
message = send(clientSocket,"TYPE A")
message = send(clientSocket,"PASV")
start = message.find("(")
end  = message.find(")")
tuple = message[start+1:end].split(',')
port = int(tuple[4])*256 + int(tuple[5])

dataSocket = socket.socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))
message = send(clientSocket, "LIST")
message = dataSocket.recv(2048)
print message
time.sleep(2)

tcpSocket = socket.socket(AF_INET, SOCK_STREAM)
tcpPort = 1717
tcpSocket.bind(('', tcpPort))
tcpSocket.listen(1)
print "CTRL-C to quit"

try:
	connectionSocket, addr = tcpSocket.accept()
	message = connectionSocket.recv(2048)
	
	if not message:
		print "Closed"
		connectionSocket.close()
	
	message = send(clientSocket, "LIST")
	
	webClient = open('FTP.html', 'r')
	clientMessage = webClient.read() + message
	
	print clientMessage

	connectionSocket.send('HTTP/1.1 200 OK\r\n')
	connectionSocket.send('Connection: closed\r\n')
	connectionSocket.send('Content-Type: text/html\n\n')
	connectionSocket.send(clientMessage)
	returnMessage = dataSocket.recv(2048)
	print returnMessage
	dataSocket.close()
	message = clientSocket.recv(2048)
	print message
	message = send(clientSocket, "QUIT")
	clientSocket.close()

except IOError:
	errorFile = open('error.html', 'r')
	message = errorFile.read()
	
	connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
	connectionSocket.send('Connection: closed\r\n')
	connectionSocket.send('Content-Type: text/html\n\n')

	connectionSocket.send(message)
	connectionSocket.close()

except KeyboardInterrupt:
	print "\nQuit using CTRL-C"
