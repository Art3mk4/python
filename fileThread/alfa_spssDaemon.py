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
import sys
import argparse

readedFile = []
activeQueue = []
path = '/srv/http/poll_ast/admin/runtime'
threadLock = threading.Lock()
exitFlag = False
workQueue = Queue.Queue(10)
threadId = 1

class FileReader(threading.Thread):
    files = []

    def __init__(self, queue):
        global activeQueue
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True

    def run(self):
        global readedFile
        global threadLock
        while not exitFlag:
            threadLock.acquire()
            self.files = iter([os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.yml')])
            for file in self.files:
                if not file in readedFile:
                    self.readFile(file)
            if self.isEnd() and readedFile != []:
                readedFile = []
                logger.info('END of Files')
            threadLock.release()

    def readFile(self, fileName):
        global readedFile
        global exitFlag
        readedFile.append(fileName)
        time.sleep(2)
        logger.info('Файл прочитан: ' + fileName)
        contentFile = open(fileName)
        params = yaml.load(contentFile)
        decodeParams = self._decode_dict(params)
        with savReaderWriter.SavWriter(decodeParams['output'], decodeParams['varNames'], decodeParams['varTypes'], decodeParams['valueLabels'], decodeParams['varLabels'], decodeParams['formats']) as writer:
            for record in decodeParams['records']:
                writer.writerow(record)
        #os.remove(fileName)
        contentFile.close()
        logger.info('Файл удалён: ' + fileName)
        logger.info('Прочитано файлов: ' + str(len(readedFile)))

    def isEnd(self):
        return self.files.__length_hint__() == 0

    def _decode_list(self, data):
        rv = []
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
            fileReader = FileReader(workQueue)
            fileReader.start()
            fileReader.run()
            fileReader.join()
            time.sleep(3)

    def on_error(self, signal, frame):
        global exitFlag
        exitFlag = True
        logger.info('Error DAEMON STOPPED')

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