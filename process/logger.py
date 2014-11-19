import time
import logging

class Eggs(object):
    def __init__(self, startvalue='green'):
        " init a spam object "
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        self.logger = logging.getLogger("DaemonLog")
        self.color  = startvalue

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def run(self):
        ' Just loop sounding happy. '
        while True:
            self.logger.info("yippie kai ai o")
            time.sleep(2)

spamalot = Eggs()
print spamalot.color
spamalot.color = 42
print spamalot.color
spamalot.run()