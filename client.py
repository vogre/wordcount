import socket

PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))

msg = "It's not what you know it's when you know it"
s.send(bytes(msg, "utf-8"))
s.close()
