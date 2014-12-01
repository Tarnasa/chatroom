<<<<<<< Updated upstream
import socket

custom_port = 49152 #ports from 49152-65535 can be used for custom purposes
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyaddr(socket.gethostname())[0]

chatroom.connect((hostname, custom_port))
chatroom.send("hello, world")

=======
import sys
import socket


serverName = raw_input('What server do you want to connect to? ex. rc02xcs213.managed.mst.edu ')
portNumber = raw_input('What port? ')
userName = raw_input('What do you want your name to be? ex. Fred ')

server_address = (str(serverName), int(portNumber))
try:
    socket.create_connection(server_address)
else:
    print('That did not work, try again. \n')
    serverName = raw_input('What server do you want to connect to? ex. rc02xcs213.managed.mst.edu ')
    portNumber = raw_input('What port? ')
>>>>>>> Stashed changes
