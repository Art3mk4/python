import time
import subprocess
import os
from daemon import runner

class Application():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.dirname(os.path.abspath(__file__)) + '/process.pid'
        self.pidfile_timeout = 1

    def run(self):
        while True:
            subprocess.call(('notify-send', 'time', time.ctime()))
            time.sleep(0.2)


app = Application()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()