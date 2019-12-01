import socket, time

WORD_STREAM_PORT = 1234
SEND_INTERVAL_SECONDS = 1
TOTAL_SEND_COUNT = 50

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), WORD_STREAM_PORT))

sendcount = 0
while True:

    if sendcount == TOTAL_SEND_COUNT:
        break

    msg = "It's not what you know it's when you know it"
    s.send(bytes(msg, "utf-8"))
    sendcount += 1
    time.sleep(SEND_INTERVAL_SECONDS)

s.close()
