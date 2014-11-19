import pprint
import xml.etree.ElementTree as ET
doc = ET.parse('spss_task_1411018198.xml')
root = doc.getroot()
pp = pprint.PrettyPrinter(depth=10)

def parseXml(node):
    d = dict()
    d.update(node.items())
    for child in list(node):
        if hasattr(node, 'text') and node.text is not None and node.text.rstrip() != '':
            d['text'] = node.text
        child.tag = child.tag.replace('item', '')
        if child.tag not in d:
            d[child.tag] = parseXml(child)
        else:
            if not isinstance(d[child.tag], list):
                d[child.tag] = [d[child.tag], parseXml(child)]
            else:
                d[child.tag].append(parseXml(child))
    return d

def readXml(node):
    d = dict()
    for child in node.getchildren():
        child.tag = child.tag.replace('item', '')
        if hasattr(child, 'text') and child.text is not None and child.text.rstrip() != '':
            d[child.tag] = child.text
        else:
            d[child.tag] = readXml(child)
    if d == {}:
        return ''
    return d

def convertToList(data):
    temp = []
    for key, value in data.iteritems():
        if isinstance(value, dict):
            temp.append(convertToList(value))
        else:
            temp.append(value)
    return temp

#help(root)
#print(root.attrib, root.items())
#for value in root.iter('records'):
#    print (value.getchildren())
params = readXml(root)

params['records'] = convertToList(params['records'])
params['varNames'] = convertToList(params['varNames'])
pp.pprint(params)
#print hoho['records'][0]