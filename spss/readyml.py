#coding: utf-8
import yaml
import pprint

config = open('hoho.yml')
params = yaml.load(config)
pp = pprint.PrettyPrinter(depth=10)
pp.pprint(params)