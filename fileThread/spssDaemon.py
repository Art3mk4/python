#!/usr/bin/env python2.7
#coding: utf-8
import os
import threading
import yaml
import savReaderWriter
import signal
from daemon import runner
from lockfile import LockTimeout
import time
import logging
import Queue

readedFile = []
threadLock = threading.Lock()
exitFlag = False
workQueue = Queue.Queue()

class FileReader(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True

    def run(self):
        global readedFile
        global exitFlag
        global workQueue
        logger.info('START THREAD:' + self.name)
        threadLock.acquire()
        if not workQueue.empty():
            fileName = self.queue.get()
            if not fileName in readedFile:
                readedFile.append(fileName)
                self.readFile(fileName)
                logger.info('Прочитан файл: ' + fileName)
        threadLock.release()
        logger.info('END THREAD: ' + self.name)

    def readFile(self, fileName):
        logger.info('Файл прочитан: ' + fileName + " Поток: " + self.name)
        contentFile = open(fileName)
        params = yaml.load(contentFile)
        decodeParams = self._decode_dict(params)
        with savReaderWriter.SavWriter(decodeParams['output'], decodeParams['varNames'], decodeParams['varTypes'], decodeParams['valueLabels'], decodeParams['varLabels'], decodeParams['formats']) as writer:
            for record in decodeParams['records']:
                writer.writerow(record)
        os.remove(fileName)
        contentFile.close()
        logger.info('Файл удалён: ' + fileName + " Поток: " + self.name)

    def _decode_list(self, data):
        rv = []
        if not data is None:
            for item in data:
                if isinstance(item, unicode):
                    item = item.encode('utf-8')
                elif isinstance(item, list):
                    item = self._decode_list(item)
                elif isinstance(item, dict):
                    item = self._decode_dict(item)
                rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        if not data is None:
            for key, value in data.iteritems():
                if isinstance(key, unicode):
                    key = key.encode('utf-8')
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                elif isinstance(value, list):
                    value = self._decode_list(value)
                elif isinstance(value, dict):
                    value = self._decode_dict(value)
                rv[key] = value
        return rv

class Application():

    files = []
    threads = []
    path = '/srv/http/poll_ast/admin/runtime'

    def __init__(self):
        self.stdin_path = '/dev/tty'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.dirname(os.path.abspath(__file__)) + '/spss.pid'
        self.pidfile_timeout = 2

    def run(self):
        global exitFlag
        global workQueue
        signal.signal(signal.SIG_IGN, self.on_error)
        signal.signal(signal.SIGTERM, self.on_error)
        logger.info('DAEMON STARTED')
        while not exitFlag:
            self.files = iter([os.path.join(self.path, file) for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file)) and file.endswith('.yml')])
            threadLock.acquire()
            if not self.isEnd():
                for file in self.files:
                    self.threadStart()
                    workQueue.put(file)
            threadLock.release()
        self.threadStop()

    def threadStart(self):
        global workQueue
        fileReader = FileReader(workQueue)
        fileReader.start()
        self.threads.append(fileReader)

    def threadStop(self):
        logger.info('Потоков создано: '+str(len(self.threads)))
        for thread in self.threads:
            thread.join()
        time.sleep(2)

    def isEnd(self):
        global readedFile
        if self.files.__length_hint__() == 0 and readedFile != []:
            readedFile = []
            self.threads = []
            return True
        return False

    def on_error(self, signal, frame):
        global exitFlag
        exitFlag = True
        logger.info('DAEMON STOPPED')

if __name__ == "__main__":
    logger = logging.getLogger("DaemonLog")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/spss.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    app = Application()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.daemon_context.files_preserve=[handler.stream]

    try:
        time.sleep(1)
        daemon_runner.do_action()
    except LockTimeout:
        print 'Daemon is runned'