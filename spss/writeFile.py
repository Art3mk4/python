#coding: utf-8
import codecs
out = file("someFile", "w")
out.write(codecs.BOM_UTF8)
out.write(u'лалалал'.encode("utf-8"))
out.close()