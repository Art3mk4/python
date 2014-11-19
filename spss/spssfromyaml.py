#coding: utf-8
import yaml
import os
import savReaderWriter

config = open('configP.yml')
params = yaml.load(config)

savFileName = 'someFile.sav'

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

params = _decode_dict(params)
with savReaderWriter.SavWriter(savFileName, params['varNames'], params['varTypes'], params['valueLabels'], params['varLabels'], params['formats']) as writer:
    for record in params['records']:
        writer.writerow(record)