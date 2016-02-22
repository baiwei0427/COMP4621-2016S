import socket

# create a socket object using TCP (SOCK_STREAM) as the transport protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP address of the server
server_ip = "143.89.40.4"
# port number
server_port = 80

# connect to the server
s.connect((server_ip, server_port))
# request content
request = 'GET / HTTP/1.0\r\n\r\n'
# send the line to the server
s.sendall(request)
response = ''
while True:
    # receive no more than 8192 bytes
    data = s.recv(8192)
    if not data:
        break
    response = response + data
# close the connection
s.close()

# print the response
print response
