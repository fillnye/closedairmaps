import xml.etree.ElementTree as ET
import json 

def Amdtscraper(x):
  try:
    if x[0].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[0]
    else:
        return x
  except IndexError:
        return x

def convertTODecimal(y, x):
    xneg = 1
    yneg = 1
    if(x[len(x)-1]=='W'):
        xneg=-1
    if(y[len(y)-1]=='S'):
        yneg=-1
    return [round(int(y[0:2])+int(y[2:4])/60.0+float(y[4:(len(y)-1)])/3600.0*yneg,11),round((int(x[0:3])+int(x[3:5])/60.0+float(x[5:(len(x)-1)])/3600)*xneg,11)]


id = -1
waypointlist = {}
f = open("SP.xhtml", "r")
tree = ET.fromstring(f.read())
osmxml = ET.Element("osm", {'version':'0.6', 'generator':'openAirWays'})
for i in tree[1][1][1][1][:-1]:
    coords = convertTODecimal(Amdtscraper(i[1][0][0]).text, Amdtscraper(i[1][1][0]).text)
    x = ET.Element("node",{'id':str(id), 'action':'modify', 'visible':'true', "lat":str(coords[0]), "lon":str(coords[1])})
    print("id:" + str(id))
    x.append(ET.Element("tag",{"k":"name","v":Amdtscraper(i[0][0]).text}))
    x.append(ET.Element("tag",{"k":"aero","v":"waypoint"}))
    print("Name:" +  Amdtscraper(i[0][0]).text)
    print("Long:" + Amdtscraper(i[1][0][0]).text)
    print("Lat:" + Amdtscraper(i[1][1][0]).text)
    waypointlist[Amdtscraper(i[0][0]).text] = id
    try:
     print("FRA:" + Amdtscraper(i[3][0]).text)
     x.append(ET.Element("tag",{"k":"aero:FRA","v":Amdtscraper(i[3][0]).text}))
    except IndexError:
     pass
    try:
     s = Amdtscraper(i[4][0][0]).text
     for j in Amdtscraper(i[4][0][0]):
        if j.tail != None:
            s += "\n" + j.tail
     x.append(ET.Element("tag",{"k":"aero:note","v":s}))
     print("Notes:" + s)
    except IndexError:
     pass
    osmxml.append(x)
    id-=1


f.close()

f = open("NAV.xhtml", "r")
tree = ET.fromstring(f.read())
for i in tree[1][1][1][1][1]:
    coords = convertTODecimal(Amdtscraper(i[4][0][0]).text, Amdtscraper(i[4][1][0]).text)
    x = ET.Element("node",{'id':str(id), 'action':'modify', 'visible':'true', "lat":str(coords[0]), "lon":str(coords[1])})
    print("id:" + str(id))
    print("Name:" +  i[0][0][0].text)
    print("Type:NAVAID")
    x.append(ET.Element("tag",{"k":"name","v":i[0][0][0].text}))
    x.append(ET.Element("tag",{"k":"aero","v":"navaid"}))
    if(i[0][1][1].tail!=None):
        if(i[0][1][1].tail=="/DME"):
            print("navaid:" + i[0][1][0].text + i[0][1][1].tail)
            x.append(ET.Element("tag",{"k":"aero:navaid","v":i[0][1][0].text + i[0][1][1].tail}))
        else:
            x.append(ET.Element("tag",{"k":"aero:navaid","v":i[0][1][0].text}))
    else:
        print("navaid:" + i[0][1].text)
        x.append(ET.Element("tag",{"k":"aero:navaid","v":i[0][1].text}))
    print("ID:" +  i[1][0].text)
    if len(i[2])==1:
        print("frequency:" + i[2][0][0].text)
        x.append(ET.Element("tag",{"k":"aero:frequency","v":i[2][0][0].text}))
    elif len(i[2][0])==4:
        print("frequency:" + i[2][0][0].text)
        print("channel:" + i[2][1][0].text)
        x.append(ET.Element("tag",{"k":"aero:frequency","v":i[2][0][0].text}))
        x.append(ET.Element("tag",{"k":"aero:channel","v":i[2][1][0].text}))
    else:
        print("channel:" + i[2][0][0].text)
        print("frequency:" + i[2][1][0].text)
        x.append(ET.Element("tag",{"k":"aero:frequency","v":i[2][1][0].text}))
        x.append(ET.Element("tag",{"k":"aero:channel","v":i[2][0][0].text}))
    print("Long:" + Amdtscraper(i[4][0][0]).text)
    print("Lat:" + Amdtscraper(i[4][1][0]).text)
    waypointlist[i[0][0][0].text] = id
    try:
     print("Ele:" + Amdtscraper(i[5][0][0]).text + " FT")
     x.append(ET.Element("tag",{"k":"ele","v":Amdtscraper(i[5][0][0]).text}))
    except IndexError:
     pass
    try:
     s = Amdtscraper(i[7][0][0]).text
     for j in Amdtscraper(i[7][0][0]):
        if j.tail != None:
            s += "\n" + j.tail
     x.append(ET.Element("tag",{"k":"aero:note","v":s}))
     print("Notes:" + s)
    except IndexError:
     pass
    osmxml.append(x)
    id-=1
    




osmxmltree = ET.ElementTree(element=osmxml)
ET.indent(osmxmltree, space="\t", level=0)
osmxmltree.write("output.osm")





