import socket
import threading

mutex = threading.Lock()

clients = []
user_names_set = set([])

def start_server():
	try:
		custom_port = 49152 #ports from 49152-65535 can be used for custom purposes
		bad_port = True
		chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		hostname = socket.gethostbyaddr(socket.gethostname())[0]

		while(bad_port): #Bind the socket to a port number
			try:
				chatroom.bind((hostname, custom_port))
			except socket.error:
				custom_port += 1
			else:
				bad_port = False
				print "Using host", "'" + hostname + "'", "and port", custom_port

		chatroom.listen(1) #begin listening for incoming requests

		while True:
			conn, address = chatroom.accept()
			if len(clients) < 10:
				user_name_exists = True
				while(user_name_exists):
					chosen_user_name = conn.recv(4096)
					if chosen_user_name not in user_names_set:
						user_name_exists = False
						user_names_set.add(chosen_user_name)#add the unique name to the list
						conn.send("True") #The user name is okay; communicate this to the client
						
						client = {}
						client['user_name'] = chosen_user_name
						client['connection'] = conn
						mutex.acquire()
						clients.append(client)
						mutex.release()
						msg_thread = threading.Thread(target=listen_for_msgs, args=(client,))
						msg_thread.start()
					else:
						conn.send("False")
						print "User name already taken"
			else:
				print "Too many clients are attempting to connect"
	except KeyboardInterrupt:
		warn_and_close(chatroom)



def listen_for_msgs(connection):
	user_has_left = False
	while(user_has_left == False):
		msg = connection['connection'].recv(4096)
		if msg == '/exit' or msg == "/quit" or msg == "/part":
			clients.remove(connection)
			connection['connection'].close()
			user_has_left = True
		
		if (user_has_left == False):
			msg = connection['user_name'] + ": " + msg
		else:
			msg = connection['user_name'] + " has left the chatroom."

		mutex.acquire()
		for client in clients:
			if client['user_name'] != connection['user_name']:
				client['connection'].send(msg)
		mutex.release()

def kill_connections():
	mutex.acquire()
	for client in clients:
		client['connection'].setblocking(0)
		client['connection'].close()
	mutex.release()


def warn_and_close(connection):
	for client in clients:
		client['connection'].send("/shutdown")

	kill_connections()




start_server()














