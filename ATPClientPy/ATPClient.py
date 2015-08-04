import socket
import ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s, keyfile='keyfile', certfile='certfile', server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1_2)
s.connect(('37.9.171.172', 4115))
# s.connect(('localhost', 4115))

message = '''ATP/0.1\nTALK TO THE HAND\nI NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE\nYOU HAVE BEEN TERMINATED\n\r\n'''

s.send(message.encode())

print(s.recv(4096).decode())

s.close()
    