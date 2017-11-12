#UDPClient.py

from socket import *
from datetime import datetime

serverName = 'localhost'
serverPort = 1717
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowercase sentence: ')

i = 0

while i <= 10: #10 = amount of pings messages

	sendtime = datetime.now()
	clientSocket.sendto(message, (serverName, serverPort))
	clientSocket.settimeout(1)
	
	try:
		modifiedMessage, addr = clientSocket.recvfrom(2048)
		endtime = datetime.now()
		rtt = endtime - sendtime
		print i
		print modifiedMessage
		print 'RTT is', rtt, '\n'
	except timeout:
		print i
		print 'Timeout'
		start = 0
		rtt = 0
	i = i + 1

clientSocket.close()

pass
