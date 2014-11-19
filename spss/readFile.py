#coding: utf-8
import codecs
fileObj = codecs.open( "config.yml", "r", "utf-8" )
u = fileObj.read()
print(u)

config = open('config.yml')
string = config.read()
print(string.encode('utf-8'))