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
						for client in clients:
							if client['user_name'] != chosen_user_name:
								client['connection'].send(chosen_user_name + " has joined the chatroom.\n")
						mutex.release()
						
						msg_thread = threading.Thread(target=listen_for_msgs, args=(client,chatroom))
						msg_thread.start()
					else:
						conn.send("False")
						print chosen_user_name, "already taken."
			else:
				print "Too many clients are attempting to connect"
	except KeyboardInterrupt:
		warn_and_close(chatroom)



def listen_for_msgs(connection, chatroom):
	user_has_left = False
	while(user_has_left == False):
		msg = connection['connection'].recv(4096)
		
		if msg == '/exit' or msg == "/quit" or msg == "/part":
			clients.remove(connection)
			connection['connection'].send("/bye")
			connection['connection'].close()
			user_names_set.remove(connection['user_name'])
			user_has_left = True

		if msg == '/bye': 
			clients.remove(connection)
			connection['connection'].close()
			user_names.set.remove(connection['user_name'])
			user_has_left = True

			if len(clients) == 0:
				chatroom.close()
				sys.exit("The server has shut down.")
		
		if (user_has_left == False):
			msg = connection['user_name'] + ": " + msg
		elif msg != '/bye':
			msg = connection['user_name'] + " has left the chatroom."
		elif msg == '/bye':
			print "Server will shut down"

		if msg != '/bye':
			mutex.acquire()
			for client in clients:
				if client['user_name'] != connection['user_name']:
					client['connection'].send(msg)
			mutex.release()

def warn_and_close(connection):
	for client in clients:
		client['connection'].send("/shutdown")


start_server()














