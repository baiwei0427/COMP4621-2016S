import socket
import threading
import gzip
import cStringIO
 
def gzip_compress(buf):
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf, compresslevel = 9)
    zfile.write(buf)
    zfile.close()
    return zbuf.getvalue()

def path_to_type(path):
	# currently, we support 5 types of files: HTML, CSS, JPG, PDF and PPTX
	type = 'text/html'
	if path.endswith('.css'):
		type = 'text/css'
	elif path.endswith('.jpg'):
		type = 'image/jpeg'
	elif path.endswith('.pdf'):
		type = 'application/pdf'
	elif path.endswith('.pptx'):
		type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
		
	return type
	
def http_header(status, type, length, content_encoding):
	header = '''HTTP/1.1 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n''' % (status, type, length)
	
	if len(content_encoding) > 0:
		header = header + 'Content-Encoding: ' + content_encoding + '\r\n'

	header = header + '\r\n'
	return header
	
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
		#whether the client supports gzip content-encoding
		enable_gzip = False	
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
			elif line.startswith('Accept-Encoding: '):
				if 'gzip' in line:
					enable_gzip = True
		
		if len(path) == 0 or len(host) == 0:
			self.socket.close()
			return
		
		try:
			# if the requested path is not specified
			if path == '/':
				path = '/index.html'
			
			# get content-type based on the requested file
			type = path_to_type(path)
			
			# find the requested file from current directory (./)				
			f = open('.'+path, 'r')
			body = f.read()
			f.close()
							
			if enable_gzip:
				body = gzip_compress(body)
				header = http_header('200 OK', type, len(body), 'gzip')
			else:
				header = http_header('200 OK', type, len(body), '')
				
			self.socket.sendall(header+body)
			self.socket.close()
		
		except:
			body = error_message(path)
			type = 'text/html'
			
			if enable_gzip:
				body = gzip_compress(body)
				header = http_header('404 Not Found', type, len(body), 'gzip')
			else:
				header = http_header('404 Not Found', type, len(body), '')
				
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