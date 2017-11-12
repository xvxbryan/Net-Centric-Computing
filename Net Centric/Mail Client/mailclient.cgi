#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
to_value = form.getvalue('to')
from_value = form.getvalue('from')
subject_value = form.getvalue('subject')
message_value = form.getvalue('message')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>To: %s</h2>" % (to_value)
print "<h2>From: %s</h2>" % (from_value)
print "<h2>Subject: %s</h2>" % (subject_value)
print "<h2>Message: %s</h2>" % (message_value)
print "</body>"
print "</html>"

from socket import socket, SOCK_STREAM, AF_INET
import time
import re, binascii
import cgi

def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
	print "</br>"
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    print "</br>"
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
	print "Sending ==> ", msg
	print "</br>"
	socket.send(msg + '\r\n')

serverName = 'smtp.cis.fiu.edu'
serverPort = 25

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 1717))
serverSocket.listen(1)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
recv=send_recv(clientSocket, None, '220')

clientName = 'Bryan'
userName=from_value.split('@')[0]
userServer=from_value.split('@')[1]
toName=to_value.split('@')[0]
toServer=to_value.split('@')[1]

#Send HELO command and print server response.
heloCommand='EHLO %s' % clientName
recvFrom = send_recv(clientSocket, heloCommand, '250')

#Send MAIL FROM command and print server response.
fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
recvFrom = send_recv(clientSocket, fromCommand, '250')

#Send RCPT TO command and print server response.
rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
recvRcpt = send_recv(clientSocket, rcptCommand, '250')

#Send DATA command and print server response.
dataCommand='DATA'
dataRcpt = send_recv(clientSocket, dataCommand, '354')

#Send message data.
send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
send(clientSocket, "From: Bryan Bastida <%s@%s>" % (userName, userServer));
send(clientSocket, "Subject: %s" % subject_value);
send(clientSocket, "To: %s@%s" % (toName, toServer));
send(clientSocket, ""); #End of headers
send(clientSocket, "Message: %s" % message_value);
send(clientSocket, "ocelot client");

#Message ends with a single period.
send_recv(clientSocket, ".", '250');
#Send QUIT command and get server response.
quitCommand='QUIT'
quitRcpt = send_recv(clientSocket, quitCommand, '221')
