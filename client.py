''' * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan

* * * * * * * * * * * * * * * * * * * * * * * * * * * * '''
import sys
import socket
import threading
import thread
import time# for time.sleep()

bad_port = True
bad_user_name = True
server_disconnected = [] #lists are thread safe in python

# Setting up connection
while(bad_port):
    try:
        serverName = raw_input('What server do you want to connect to? ex. rc02xcs213.managed.mst.edu ')
        portNumber = raw_input('What port? ')
        sock = socket.create_connection((str(serverName), int(portNumber)))
    except socket.error , msg:
        print 'Binding failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
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
    if sock.recv(4096) == 'True':
        bad_user_name = False
        print 'Welcome ' + userName + '\n'
    else:
        print 'Server said that ' + userName + ' is already in use. Try another one.\n'

def startClient():
    send_hold = True
    while send_hold:
        try:
            # Message Sending
            message = raw_input()
            if message == '/exit' or message == '/quit' or message == '/part':
                sock.sendall(message)#server handels any of these messages
                clientShutdown()
                send_hold = False
            elif len(server_disconnected) == 0:
                sock.sendall(message)
            elif len(server_disconnected) == 1:
                sys.exit("Goodbye.")
        except KeyboardInterrupt:
            print('\n\n### Sorry, but to shut down please type one of these and press enter: /exit, /quit, or /part instead.\n')
        except socket.error, e:
            print "WINNING"

# Gracefully closes the threads
# def closeThreads():
#     for t in threading.enumerate():
#         t.join()

def clientShutdown():
    sock.settimeout(0)# Stops recv() from waiting for more messages
    sock.close()
    sys.exit('\nYou have left the chatroom.\n')

def close_connection():
    sock.close()
    print("Server now disconnected. Press any key to exit the program.")
    server_disconnected.append(True)

# Message Send Function
def readMessage():
    read_hold = True
    while read_hold:
        recvMessage = sock.recv(4096)
        if recvMessage == '/shutdown':
            read_hold = False
            close_socket_wait = threading.Timer(1, close_connection)
            print("Server disconnecting. Connection will close after 10 seconds... ")
            close_socket_wait.start()
        elif recvMessage == '/bye':
            read_hold = False
        else:
            print recvMessage

readingThread = threading.Thread(target=readMessage)
readingThread.start()
startClient()