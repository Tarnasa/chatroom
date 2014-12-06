''' * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan

* * * * * * * * * * * * * * * * * * * * * * * * * * * * '''


import sys
import socket
import threading
import time# for time.sleep()
import signal

bad_port = True
bad_user_name = True

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
    sock.send(userName)
    print 'here!'
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
                sock.send(message)#server handels any of these messages
                clientShutdown()
                send_hold = False
            else:
                sock.send(message)
        except KeyboardInterrupt:
            print('\n\n### Sorry, but to shut down please type one of these and press enter: /exit, /quit, or /part instead.\n')

# Gracefully closes the threads
# def closeThreads():
#     for t in threading.enumerate():
#         t.join()

def clientShutdown():
    sock.settimeout(0)
    sock.close()
    # closeThreads()
    sys.exit('\nYou have left the chatroom.\n')

def serverShutdown():
    print('\nConnection will close in 10 seconds...\n')
    time.sleep(10)
    sock.settimeout(0)
    sock.close()
    # closeThreads()
    sys.exit('\nThe server has shutdown\n')

# Message Send Function
def readMessage():
    read_hold = True
    while read_hold:
        recvMessage = sock.recv(4096)
        if recvMessage == '/shutdown':
            read_hold = False
            shutdownThread = threading.Thread(target=serverShutdown)
            shutdownThread.start()
        else:
            print recvMessage


readingThread = threading.Thread(target=readMessage)
readingThread.start()
startClient()