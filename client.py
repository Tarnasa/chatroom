import sys
import socket

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

# Setting up user name
while(bad_user_name):
    try:
        userName = raw_input('What do you want your name to be? ex. Fred ')
        sock.sendall(userName)
    except socket.recv(), e:
        print 'Server said that ' + userName + ' is already in use. Try another one.\n'
    else:
        bad_user_name = False

