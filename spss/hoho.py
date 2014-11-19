#coding: utf-8
import yaml
import os

config = open('config.yml')
params = yaml.load(config)
print(params['valueLabels'])

def addBinaryKeys():
    for key in params['varTypes'].keys():
        params['varTypes'][key] = {"b'"+key+"'": 'hoho'}

keys = addBinaryKeys()
print(params['varTypes'])