import os

PluginFolder = "libs"
MainModule = "__init__"

def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        filename, fileExtension = os.path.splitext(i)
        if os.path.isdir(location) or fileExtension != ".py" or filename == MainModule:
            continue
        moduleName = PluginFolder + '.' + filename
        package = __import__(moduleName)
        object = getattr(package, filename)
        plugins.append({"name": filename, "object":object})
    return plugins

for i in getPlugins():
    print("Loading plugin " + i["name"])
    print(getattr(i["object"], "x", None))
    print(getattr(i["object"], "y", None))

""""
import libs
from libs import *
print(lib1.x + lib2.y)
"""