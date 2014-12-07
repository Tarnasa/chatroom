import socket
import threading
import sys

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
						
						conn.sendall("True") #The user name is okay; communicate this to the client
						client = {}
						client['user_name'] = chosen_user_name
						client['connection'] = conn
						
						mutex.acquire()
						clients.append(client)
						for client in clients:
							if client['user_name'] != chosen_user_name:
								client['connection'].sendall(chosen_user_name + " has joined the chatroom.\n")
						mutex.release()
						
						msg_thread = threading.Thread(target=listen_for_msgs, args=(client,chatroom))
						msg_thread.start()
					else:
						conn.sendall("False")
						print chosen_user_name, "already taken."
			else:
				print "Too many clients are attempting to connect"
	except KeyboardInterrupt:
		warn_and_close(chatroom)



def listen_for_msgs(connection, chatroom):
	user_has_left = False
	server_closing = False

	while(user_has_left == False and server_closing == False):
		msg = connection['connection'].recv(4096)

		if len(msg) == 0:
			clients.remove(connection)
			user_names_set.remove(connection['user_name'])
			
			if len(clients) == 0:
				chatroom.close()
			
			server_closing = True
			print "Chatroom closed."

		if msg == '/exit' or msg == "/quit" or msg == "/part":
			mutex.acquire()
			clients.remove(connection)
			mutex.release()

			connection['connection'].sendall("/bye")
			connection['connection'].close()
			user_names_set.remove(connection['user_name'])
			user_has_left = True

		if (user_has_left == False):
			msg = connection['user_name'] + ": " + msg
		elif (user_has_left == True):
			msg = connection['user_name'] + " has left the chatroom."

		if (server_closing != True):
			mutex.acquire()
			for client in clients:
				if client['user_name'] != connection['user_name']:
					client['connection'].sendall(msg)
			mutex.release()


def warn_and_close(connection):
	for client in clients:
		client['connection'].sendall("/shutdown")

start_server()














