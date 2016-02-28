import socket


# Note that in python 3.X, we should use input instead of raw_input
line = raw_input("Please input a line:")

# create a socket object using TCP (SOCK_STREAM) as the transport protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP address of the server
server_ip = "127.0.0.1"
# port number
server_port = 12345

# connect to the server
s.connect((server_ip, server_port))
# send the line to the server
s.send(line)
# receive no more than 1024 bytes
result = s.recv(1024)
# close the connection
s.close()

# print the line sent by the server
print result
