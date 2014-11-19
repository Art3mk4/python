import os
import subprocess
import time
from daemonize import Daemonize

pid = os.path.dirname(os.path.abspath(__file__)) + '/process.pid'


def main():
    while True:
        subprocess.call(('notify-send', 'time', time.ctime()))
        time.sleep(1)

daemon = Daemonize(app="hoho", pid=pid, action=main)
daemon.start()