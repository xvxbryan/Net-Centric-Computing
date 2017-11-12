#TCPServer.py

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
		
		filename = message.split()[1].partition("/")[2]

		file = open(filename, 'rU').read()
		
		connectionSocket.send('HTTP/1.1 200 OK\n')		
		connectionSocket.send('Content-type: text/plain\n')
		connectionSocket.send('\n')
		connectionSocket.send(file)
		connectionSocket.close()
	
	except IOError:
		
		file = open('error.html', 'r')
		message = file.read()
		print "404 Not Found"
		connectionSocket.send('\HTTP/1.1 404 Not Found\n')
		connectionSocket.send('Content-type: text/plain\n\n')
		connectionSocket.send(message)
		connectionSocket.close()
	except KeyboardInterrupt:
		print "\nInterrupted by CTRL-C"
		break
serverSocket.close()
