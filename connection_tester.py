import socket

custom_port = 49152 #ports from 49152-65535 can be used for custom purposes
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyaddr(socket.gethostname())[0]

chatroom.connect((hostname, custom_port))
chatroom.send("hello, world")

