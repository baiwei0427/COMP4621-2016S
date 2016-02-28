import socket


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

while True:
    # establish a connection
    client_socket, addr = s.accept()
    # receive no more than 1024 bytes from the client
    line = client_socket.recv(1024)
    # send the reversed line to the client
    client_socket.send(line[::-1])
    # close the connection
    client_socket.close()
	# print information
    print "Receive %s from %s" % (line, str(addr))
