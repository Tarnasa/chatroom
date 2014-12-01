import socket

custom_port = 49153 #ports from 49152-65535 can be used for custom purposes
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = raw_input('what is the host? ')

chatroom.connect((hostname, custom_port))
chatroom.send("hello, luke")

