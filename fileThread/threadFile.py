import os
import threading
import time

class FileReader(threading.Thread):
    files = []
    path = '/srv/http/python/fileThread'

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        global readedFile
        global threadLock
        threadLock.acquire()
        self.files = [os.path.join(self.path, file) for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file)) and file.endswith('.yml')]

        for file in iter(self.files):
            if not file in readedFile:
                self.readFile(file)
        if len(self.files) == len(readedFile) and readedFile != []:
            readedFile = []
            print('END')
        print len(readedFile)
        threadLock.release()

    def readFile(self, fileName):
        global readedFile
        readedFile.append(fileName)
        print(fileName)

readedFile = []
threadLock = threading.Lock()

if __name__ == '__main__':
    while True:
        fileReader = FileReader()
        fileReader.run()