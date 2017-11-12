#UDPClient.py

from socket import socket, SOCK_DGRAM, AF_INET
import datetime

serverName = 'localhost'
serverPort = 1717
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowercase sentence: ')

sendtime = datetime.datetime.now()

clientSocket.sendto(message, (serverName, serverPort))

clientSocket.settimeout(1)

modifiedMessage, addr = clientSocket.recvfrom(2048)
receivetime = datetime.datetime.now()
rtt = receivetime.microsecond - sendtime.microsecond
print "Message", modifiedMessage, addr

print "RTT: %d ms" % rtt

clientSocket.close()
