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
        
        try:
            portNumber = input('What port? ')
        except NameError:
            print "Port must be a number."
            portNumber = -1

        sock = socket.create_connection((str(serverName), portNumber))
    except socket.error , msg:
        print 'Binding failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
    else:
        bad_port = False
        print 'You successfully connected to ' + serverName + ' on port ' + str(portNumber) + '\n'

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
            message = raw_input("You: ")
            if message == '/exit' or message == '/quit' or message == '/part':
                sock.sendall(message)#server handels any of these messages
                send_hold = False
            if message == '/connection_closed':
                sock.sendall('/connection_closed/') #replace this so the user doesn't accidentally send an admin command
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
    sock.close()
    sys.exit('\nYou have left the chatroom.\n')

def close_connection():
    sock.sendall('/connection_closed')
    sock.close()
    server_disconnected.append(True)
    print("Server now disconnected. Press any key to exit the program.")
    

# Message Send Function
def readMessage():
    read_hold = True
    while read_hold and len(server_disconnected) == 0:
        recvMessage = sock.recv(4096)
        
        if recvMessage == '/shutdown':
            close_socket_wait = threading.Timer(10, close_connection)
            print("Server disconnecting. Connection will close after 10 seconds... ")
            close_socket_wait.start()
        
        #the server has received the shutdown request, and removed the client from its list of open clients
        elif recvMessage == '/bye': 
            read_hold = False
            sock.close()
        else:
            print recvMessage

readingThread = threading.Thread(target=readMessage)
readingThread.start()
startClient()