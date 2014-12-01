import socket


custom_port = 49152 #ports from 49152-65535 can be used for custom purposes
bad_port = True
chatroom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyaddr(socket.gethostname())[0]

while(bad_port): #Bind the socket to a port number
	try:
		chatroom.bind((hostname, custom_port))
	except socket.error, e:
		custom_port += 1
	else:
		bad_port = False
		print "Using host", "'" + hostname + "'", "and port", custom_port

chatroom.listen(4) #begin listening for incoming requests

conn, address = chatroom.accept()









