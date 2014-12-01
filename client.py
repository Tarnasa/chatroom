''' * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan

* * * * * * * * * * * * * * * * * * * * * * * * * * * * '''


import sys
import socket
import threading

bad_port = True
bad_user_name = True

# Setting up connection
while(bad_port)
    try:
        serverName = raw_input('What server do you want to connect to? ex. rc02xcs213.managed.mst.edu ')
        portNumber = raw_input('What port? ')
        sock = socket.create_connection((str(serverName), int(portNumber)))
    except socket.error , msg:
        print 'Binding failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
    else:
        bad_port = False
        print 'You successfully connected to ' + serverName + ' on port ' + portNumber + '\n'

# First server response is True (<= 10 users connected) or False (> 10 users connected, show error msg)
# if sock.recv(1) is False:
#     print 'Sorry too many users already, try again later.\n'

# Setting up user name
while(bad_user_name):
        userName = raw_input('What do you want your name to be? ex. Fred ')
        sock.sendall(userName)
        print 'Server said that ' + userName + ' is already in use. Try another one.\n'
    if sock.recv(1) is True:
        bad_user_name = False

