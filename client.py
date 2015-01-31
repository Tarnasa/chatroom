''' * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan
  File Description: The client side of the chatroom

* * * * * * * * * * * * * * * * * * * * * * * * * * * * '''
import sys
import socket
import threading


server_disconnected = []  # lists are thread safe in python

# Setting up connection
def set_up_connection():
    bad_port = True
    while (bad_port):
        try:
            serverName = input('Server (i.e. rc02xcs213.managed.mst.edu): ')

            try:
                portNumber = int(input('Port: '))
            except NameError:
                print("Port must be a number.")
                portNumber = -1

            sock = socket.create_connection((str(serverName), portNumber))
        except socket.error as msg:
            print('Binding failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
        else:
            bad_port = False
            print('You successfully connected to ' + serverName + ' on port ' + str(portNumber) + '\n')
    return sock


def get_user_name(conn):
    bad_user_name = True
    while (bad_user_name):
        userName = input('Choose a user name (i.e. Fred): ')
        conn.send(userName.encode('utf-8'))
        valid_name = conn.recv(4096).decode('utf-8')
        if "True" in valid_name:
            bad_user_name = False
            total_users = valid_name.split(',')[1]
            print('Welcome', userName + "!", "There are currently", total_users, "other users logged on.\n")
            print("To send a message, simply type your message and hit enter.")
        elif "False" in valid_name:
            print('Server said that ' + userName + ' is already in use. Try another one.\n')
        elif "/too_many" in valid_name:
            sys.exit("Too many users currently connected. Try again later. Goodbye.")


def startClient(conn):
    send_hold = True
    while send_hold:
        try:
            # Message Sending
            message = input()
            if message == '/exit' or message == '/quit' or message == '/part':
                send_hold = False
            if message == '/connection_closed':
                conn.send('/connection_closed/'.encode(
                    'utf-8'))  # replace this so the user doesn't accidentally send an admin command
            elif len(server_disconnected) == 0:
                conn.send(message.encode('utf-8'))
            elif len(server_disconnected) == 1:
                sys.exit("Goodbye.")
        except KeyboardInterrupt:
            print('\n\n### Sorry, but to shut down please type one of these and press enter: /exit, /quit, or /part\n')
        except socket.error as e:
            print("WINNING")


def clientShutdown(conn):
    conn.close()
    sys.exit('\nYou have left the chatroom.\n')


def close_connection(conn):
    conn.send('/connection_closed'.encode('utf-8'))
    conn.close()
    server_disconnected.append(True)
    print("Server now disconnected. Press any key to exit the program.")


# Message Send Function
def readMessage(conn):
    read_hold = True
    while read_hold and len(server_disconnected) == 0:
        recvMessage = conn.recv(4096).deocde('utf-8')
        if recvMessage == '/shutdown':
            close_socket_wait = threading.Timer(10, close_connection, (conn,))
            print("Server disconnecting. Connection will close after 10 seconds... ")
            close_socket_wait.start()

        # the server has received the shutdown request, and removed the client from its list of open clients
        elif recvMessage == '/bye':
            read_hold = False
            conn.close()
            print("Goodbye.")
        else:
            print(recvMessage)


sock = set_up_connection()
get_user_name(sock)
readingThread = threading.Thread(target=readMessage, args=(sock,))
readingThread.start()
startClient(sock)