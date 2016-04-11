import socket
import threading

def http_header(status, length):
	return '''HTTP/1.1 %s\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n''' % (status, length)
	
def error_message(path):
	return '''<html>
	<head><title>404 Not Found</title></head>
	<body><h1>Not Found</h1>
	<p>The requested URL %s was not found on this server.</p>
	</body></html>''' % path
	
class ServerThread(threading.Thread):
	def __init__(self, client_socket, addr):
		self.socket = client_socket
		self.addr = addr 
		threading.Thread.__init__(self)
	
	def run(self):
		request = ''
		while True:
			data = self.socket.recv(1024)
			if data:
				request = request + data
				if data.endswith('\r\n\r\n'):
					break
			else: 
				break
		
		request_lines = request.split('\r\n')
		if len(request_lines) < 3:
			self.socket.close()
			return 
		
		path = ''
		if request_lines[0].startswith('GET '):
			lines = request_lines[0].split(' ')
			if (len(lines) >= 2):
				path = lines[1]
		
		host = ''
		for line in request_lines:
			if line.startswith('Host: '):
				host = line[6:]
		
		if len(path) == 0 or len(host) == 0:
			self.socket.close()
			return
		
		try:
			# find the requested file from current directory (./)
			f = open('.'+path, 'r')
			body = f.read()
			f.close()
			header = http_header('200 OK', len(body))
			self.socket.sendall(header+body)
			self.socket.close()
		except:
			body = error_message(path)
			header = http_header('404 Not Found', len(body))
			self.socket.sendall(header+body)
			self.socket.close()

# create a socket object using TCP (SOCK_STREAM) as the transport protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP address of the server
server_ip = "0.0.0.0"
# port number
server_port = 8080

# bind socket to local address
s.bind((server_ip, server_port))
# queue up to 5 requests
s.listen(5)

while True:
	# establish a connection
	client_socket, addr = s.accept()
	t = ServerThread(client_socket, addr)
	t.start() 