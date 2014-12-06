import socket
import threading

<<<<<<< HEAD
custom_port = input("port: ") #ports from 49152-65535 can be used for custom purposes
=======
custom_port = 49153 #ports from 49152-65535 can be used for custom purposes
>>>>>>> 9b700594e98fe82269900704525db731d8578a38
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = raw_input('what is the host? ')

chatroom.connect((hostname, custom_port))
<<<<<<< HEAD

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


=======
chatroom.send("hello, luke")
>>>>>>> 9b700594e98fe82269900704525db731d8578a38

