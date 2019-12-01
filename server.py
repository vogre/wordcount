import socket, threading, pickle

WORD_STREAM_PORT = 1234
GET_COUNT_PORT = 4321
DELIMITER = ' '
wordCount = {}

class WordStreamThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket

    def saveWord(self, word):
        lword = word.lower()
        if lword in wordCount:
            wordCount[lword] += 1
        else:
            wordCount[lword] = 1

    def run(self):
        currentWord = ''
        while True:
            buffer = self.csocket.recv(20000)

            if len(buffer) <= 0:
                if len(currentWord) > 0:
                    self.saveWord(currentWord)
                break

            text = buffer.decode("utf-8")

            for char in text:
                if char == DELIMITER:
                    self.saveWord(currentWord)
                    currentWord = ""
                else:
                    currentWord += char

            # Cut words at end of buffer
            if len(currentWord) > 0:
                self.saveWord(currentWord)
                currentWord = ''

def listen():
    wordstreamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wordstreamSocket.bind((socket.gethostname(), WORD_STREAM_PORT))
    wordstreamSocket.listen()

    clientSocket, clientAddress = wordstreamSocket.accept()
    thread = WordStreamThread(clientAddress, clientSocket)
    thread.start()

    # Listen to get socket
    getcountSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    getcountSocket.bind((socket.gethostname(), GET_COUNT_PORT))
    getcountSocket.listen()

    while True:
        getcountClient, getCountAddress = getcountSocket.accept()
        wordCountBytes = pickle.dumps(wordCount)
        getcountClient.send(wordCountBytes)
        getcountClient.close()


# Execution starts here
listen()
