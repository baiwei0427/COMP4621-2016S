import socket
import threading

class ServerThread(threading.Thread):
	def __init__(self, client_socket, addr, lock):
		self.socket = client_socket
		self.addr = addr 
		self.lock = lock
		threading.Thread.__init__(self)
	
	def run(self):
		# receive no more than 1024 bytes from the client
		line = self.socket.recv(1024)
		# send the reversed line to the client
		self.socket.send(line[::-1])
		# close the connection
		self.socket.close()
		self.lock.acquire()
		# print information
		print "Receive %s from %s" % (line, str(self.addr))
		self.lock.release()
	
	
# create a socket object using TCP (SOCK_STREAM) as the transport protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP address of the server
server_ip = "127.0.0.1"
# port number
server_port = 12345

# bind socket to local address
s.bind((server_ip, server_port))
# queue up to 5 requests
s.listen(5)
# We need a lock for multiple threads 
lock = threading.Lock()

while True:
	# establish a connection
	client_socket, addr = s.accept()
	t = ServerThread(client_socket, addr, lock)
	t.start() 

