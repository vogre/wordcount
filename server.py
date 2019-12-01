import socket

PORT = 1234
DELIMITER = ' '
wordCount = {}

def saveWord(word):
    if word in wordCount:
        wordCount[word.lower()] += 1
    else:
        wordCount[word.lower()] = 1

def printWords():
    for x, y in wordCount.items():
        print(x, y)

def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), PORT))
    s.listen()

    client, address = s.accept()

    currWord = ""

    while True:
        buffer = client.recv(20000)

        if len(buffer) <= 0:
            if len(currWord) > 0:
                saveWord(currWord)
            s.close()
            break

        text = buffer.decode("utf-8")

        for char in text:
            if char == DELIMITER:
                saveWord(currWord)
                currWord = ""
            else:
                currWord += char

    printWords()


# Execution starts here
listen()
