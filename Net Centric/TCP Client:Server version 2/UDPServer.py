#UDPServer.py

from socket import socket, SOCK_DGRAM, AF_INET
import random
import time
#Create a UDP socket 
#Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 1717))

print "Waiting for connections"

while True:
	
	rnd = random.randint(0,10)

	# Receive the client packet along with the address it is coming from
	message, address = serverSocket.recvfrom(2048)

	# Capitalize the message from the client
	print message, address
	message = message.upper()
	
	if rnd < 4:
		continue
	time.sleep(.05)
	serverSocket.sendto(message, address)
serverSocket.close()
