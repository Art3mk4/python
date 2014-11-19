import argparse
import os
class StartAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print "Hello"
        print(values)
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', action=StartAction)
print os.getcwd().split(os.path.realpath(__file__))[0], os.path.realpath(__file__).split(os.sep), os.getcwd()