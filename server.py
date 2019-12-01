import socket, threading, pickle

WORD_STREAM_PORT = 1234
GET_COUNT_PORT = 4321
DELIMITER = ' '
wordCount = {}

class WordStreamThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def saveWord(self, word):
        lword = word.lower()
        if lword in wordCount:
            wordCount[lword] += 1
        else:
            wordCount[lword] = 1

    def run(self):

        while True:
            cSocket, cAddress = self.socket.accept()
            currentWord = ''
            while True:
                buffer = cSocket.recv(20000)

                if len(buffer) <= 0:
                    cSocket.close()
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

class GetCountThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            getcountClient, getCountAddress = self.socket.accept()
            wordCountBytes = pickle.dumps(wordCount)
            getcountClient.send(wordCountBytes)
            getcountClient.close()

def Main():
    wordstreamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wordstreamSocket.bind((socket.gethostname(), WORD_STREAM_PORT))
    wordstreamSocket.listen(10)

    wordStreamThread = WordStreamThread(wordstreamSocket)
    wordStreamThread.start()

    getcountSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    getcountSocket.bind((socket.gethostname(), GET_COUNT_PORT))
    getcountSocket.listen(10)

    getCountThread = GetCountThread(getcountSocket)
    getCountThread.start()


# Execution starts here
Main()
