''' * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan
  File Description: Server side of the chatroom

* * * * * * * * * * * * * * * * * * * * * * * * * * * * '''
import socket
import threading
import _thread
import sys
import errno

thread = _thread

mutex = threading.Lock()

clients = [] 
user_names_set = set([])

def start_server():
	try:
		custom_port = 49152 #ports from 49152-65535 can be used for custom purposes
		bad_port = True
		chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket with the address family AF_INET and socket type SOCK_STREAM
		
		hostname = socket.gethostbyname(socket.gethostname()) #The current machine becomes the server

		while(bad_port and custom_port < 65536): #Bind the socket to a port number that is not already taken
			try: #try binding with the given port number
				chatroom.bind((hostname, custom_port))
			except socket.error: #if it is already taken, 
				custom_port += 1 #increment the port number by 1
			else:
				bad_port = False
				print("Using host", "'" + hostname + "'", "and port", custom_port)
		
		if custom_port == 65536:
			sys.exit("Error: Unable to find a port that is not already taken. Something has gone wrong...")

		try:
			chatroom.listen(4) #begin listening for incoming requests.
		except socket.error as e:
			print(e)
			sys.exit("Chatroom unable to listen for connections. Ending program.")

		while True: #Always accept new connections
			try:
				conn, address = chatroom.accept() #conn is the socket, address is a tuple of (host, port)
			except socket.error as e:
				print(e)
				sys.exit("Unable to accept connection. Ending program")

			if len(clients) < 10:
				user_name_exists = True
				while(user_name_exists):
					try:
						chosen_user_name = conn.recv(4096).decode('utf-8') #the first message from the client is the name
					except socket.error as e:
						if e.errno == errno.ECONNRESET:
							print("Client quit before entering a user name")
							break
					
					if chosen_user_name not in user_names_set:
						user_name_exists = False
						
						conn.send(("True," + str(len(clients))).encode('utf-8')) #Communicate to the client that the name is not taken
						client = {}
						client['user_name'] = chosen_user_name
						client['connection'] = conn
						
						print(chosen_user_name + " has joined the chatroom.")
						
						mutex.acquire()
						clients.append(client)
						for client in clients:
							if client['user_name'] != chosen_user_name:
								client['connection'].send((chosen_user_name + " has joined the chatroom.\n").encode('utf-8'))
						user_names_set.add(chosen_user_name)#add the unique name to the list
						mutex.release()
						
						try:
							msg_thread = threading.Thread(target=listen_for_msgs, args=(client,chatroom))
							msg_thread.start() #Begin a new thread that listens for messages from this client
						except thread.error as e:
							print(e)
							sys.exit("Unable to start listening thread. Ending program.")

					else:
						conn.send("False".encode('utf-8')) #Communicate to the client that the name is taken
						print(chosen_user_name, "already taken.")
			else:
				print("Too many clients are attempting to connect")
				conn.send("/too_many".encode('utf-8'))
	except KeyboardInterrupt:
		print("\nServer has initiated shutdown")
		warn_and_close(chatroom)

def listen_for_msgs(connection, chatroom):
	user_has_left = False #if the user sends /exit, /quit, or /part, this will be set to true
	server_closing = False

	while(user_has_left == False and server_closing == False):
		try:
			msg = connection['connection'].recv(4096).decode('utf-8')
			print(msg)
			if msg == '/connection_closed': #A client will send /connection_closed to acknowledge the server shutdown.s
				mutex.acquire()
				clients.remove(connection)
				user_names_set.remove(connection['user_name'])
				mutex.release()
				
				if len(clients) == 0: #If all clients have acknowledged the shutdown and themselves closed, the chatroom can close
					chatroom.close()
					print("Goodbye.")
					sys.exit()
				
				server_closing = True

			if msg == '/exit' or msg == "/quit" or msg == "/part":
				mutex.acquire()
				clients.remove(connection)
				user_names_set.remove(connection['user_name'])
				mutex.release()
				connection['connection'].send("/bye".encode('utf-8')) #Tell the client that it is no longer listening to it. The client will disconnect itself
				user_has_left = True
			
			if msg == '/connection_closed/': #used so the user doesn't inadvertantly send an admin command
				msg = '/connection_closed'

			if (user_has_left == False):
				msg = connection['user_name'] + ": " + msg
			elif (user_has_left == True):
				msg = connection['user_name'] + " has left the chatroom."

			if (server_closing == False):
				print(msg)
				mutex.acquire()
				for client in clients:
					if client['user_name'] != connection['user_name']:
						client['connection'].send(msg.encode('utf-8'))
				mutex.release()

		except socket.error as e:
			if e.errno == errno.ECONNRESET:
				print(e)
				user_has_left = True
				print("No longer listening to", connection['user_name'])

				mutex.acquire()
				clients.remove(connection)
				user_names_set.remove(connection['user_name'])
				mutex.release()
			elif e.errno == errno.EPIPE:
				print(e)
				user_has_left = True
				print("No longer listening to", connection['user_name'])

				mutex.acquire()
				clients.remove(connection)
				user_names_set.remove(connection['user_name'])
				mutex.release()



def warn_and_close(connection):
	if len(clients) == 0:
		print("No clients connected. Goodbye.")
	else:
		for client in clients:
			client['connection'].send("/shutdown".encode('utf-8'))

start_server()
