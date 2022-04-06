import xml.etree.ElementTree as ET

def Amdtscraper(x):
  try:
    if x[0].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[0]
    else:
        return x
  except IndexError:
        return x


id = -1
f = open("SP.xhtml", "r")
tree = ET.fromstring(f.read())
osmxml = ET.Element(osm, {'version':'0.6', 'generator':'openAirWays'})
for i in tree[1][1][1][1][:-1]:
    x = ET.Element(node,{'id':str(id), 'action':'modify', 'visible':'true'})
    print("id:" + str(id))
    print("Name:" +  Amdtscraper(i[0][0]).text)
    print("Long:" + Amdtscraper(i[1][0][0]).text)
    print("Lat:" + Amdtscraper(i[1][1][0]).text)
    try:
     print("FRA:" + Amdtscraper(i[3][0]).text)
    except IndexError:
     pass
    try:
     s = Amdtscraper(i[4][0][0]).text
     for j in Amdtscraper(i[4][0][0]):
        if j.tail != None:
            s += "\n" + j.tail
     print("Notes:" + s)
    except IndexError:
     pass
    osmxml.append(x)
    id-=1

osmxmltree = ET.ElementTree(element=osmxml)
osmxmltree.write("output.xml")
