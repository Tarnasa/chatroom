import socket
import threading

custom_port = input("port: ") #ports from 49152-65535 can be used for custom purposes
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyaddr(socket.gethostname())[0]

chatroom.connect((hostname, custom_port))

def listen_for_messages(connection):
	while(True):
		print connection.recv(4096)

user_name = raw_input("User name: ")
chatroom.send(user_name)

while True:
	listen_thread = threading.Thread(target=listen_for_messages, args=(chatroom,))
	listen_thread.start()

	msg = raw_input("Msg: ")
	chatroom.send(msg)



