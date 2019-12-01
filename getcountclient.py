import socket, pickle

GET_COUNT_PORT = 4321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), GET_COUNT_PORT))

msg = s.recv(20000)
wordCount = pickle.loads(msg)
for x, y in wordCount.items():
    print(x, y)

s.close()
