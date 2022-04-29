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

def findName(k,i):
    if i[2][k][1][0].tag == "{http://www.w3.org/1999/xhtml}strong":
       return i[2][k][1][0][0].text
    else:
        return i[2][k][1][0].text


def Amdtscraper2(x,index):
  i = index*2
  try:
    if x[index].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[index][0]
    else:
        return x[i]
  except IndexError:
        return x[i]


id = -1
waypointlist = ["NULL"]
f = open("SP.xhtml", "r")
tree = ET.fromstring(f.read())
osmxml = ET.Element("osm", {'version':'0.6', 'generator':'openAirWays'})
for i in tree[1][1][1][1][:-1]:
    coords = convertTODecimal(Amdtscraper(i[1][0][0]).text, Amdtscraper(i[1][1][0]).text)
    x = ET.Element("node",{'id':str(id), 'action':'modify', 'visible':'true', "lat":str(coords[0]), "lon":str(coords[1])})
    print("id:" + str(id))
    x.append(ET.Element("tag",{"k":"name","v":Amdtscraper(i[0][0]).text}))
    x.append(ET.Element("tag",{"k":"aero","v":"waypoint"}))
    print(Amdtscraper(i[0][0]).text)
    print("Name:" +  Amdtscraper(i[0][0]).text)
    print("Long:" + Amdtscraper(i[1][0][0]).text)
    print("Lat:" + Amdtscraper(i[1][1][0]).text)
    waypointlist.insert(id*-1,Amdtscraper(i[0][0]).text)
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
    waypointlist.insert(id*-1,i[0][0][0].text)
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
    
f.close()

f = open("ENR.xhtml", "r")
tree = ET.fromstring(f.read())
a = 1
b = 1

print(waypointlist)

for i in tree[1][1][1:]:
  k = 1
  y = ""
  route = i[2][0][0][0][0].text
  for j in i[2][1:]:
      if Amdtscraper(j[0]).text == "∆" or j[0].text == " " or Amdtscraper(j[0]).text == "▲":
       if j[1][0].tag == "{http://www.w3.org/1999/xhtml}strong":
        print("Type: NAVAID")
        print(k)
        y = i[2][k][1][0][0].text
        print(i[2][k][1][0][0].text)
        print("Name: " + j[1][0][0].text)
       else:
        print("Type: Waypoint")
        y = i[2][k][1][0].text
        print(i[2][k][1][0].text)
        print("Name:" + j[1][0].text)
       if Amdtscraper(j[0]).text == "▲":
        print("flyover=true")
       #print("Coord 1 " + j[2][0].text)
       #print("Coord 2 " + j[2][2].text)
       if j[4].text != " ":
           print("Notes: " + j[4][0].attrib["title"].split("\n")[1].strip())
      elif j[0][0].text!="(RNAV)":
        x = ET.Element("way",{'id':str(id), 'action':'modify', 'visible':'true'})
        x.append(ET.Element("nd",{"ref":str(waypointlist.index(findName(k-1,i))*-1)}))
        x.append(ET.Element("nd",{"ref":str(waypointlist.index(findName(k+1,i))*-1)}))
        x.append(ET.Element("tag",{"k":"aero","v":"leg"}))
        x.append(ET.Element("tag",{"k":"name","v":route}))
        print("Type Leg")
        print("RNP: " + j[0][0].text)
        if Amdtscraper(j[1][0][0][0][0][0][0]).text == "- ":
          print("DP1: -")
        else:
          print("DP1: " + Amdtscraper(j[1][0][0][0][0][0][0][0]).text)
        if Amdtscraper(j[1][0][0][0][1][0][0]).text == " -":
          print("DP2: -")
        else:
          print("DP2: " + Amdtscraper(j[1][0][0][0][1][0][0][0]).text)
        print("DP3: " + Amdtscraper(j[2][0][0]).text)
        print("DP4: " + Amdtscraper(j[3][0][0][0][0][0][0][0]).text + " " + Amdtscraper2(j[3][0][0][0][0][0][0],1).text)
        print("DP5: " + Amdtscraper(j[3][0][0][0][1][0][0][0]).text + " " + Amdtscraper2(j[3][0][0][0][1][0][0],1).text)
        if j[4].text != " " and len(j[4])<7:
           print("DP6: " + j[4][0].text)
           print("DP7: " + Amdtscraper(j[4][1][0][0][0][0][0]).text + " " + Amdtscraper2(j[4][1][0][0][0][0],1).text)
           print("DP8: " + Amdtscraper(j[4][1][0][0][1][0][0]).text + " " + Amdtscraper2(j[4][1][0][0][1][0],1).text)
        else:
           print("DP6: -")
           print("DP7: -")
           print("DP8: -")
        if j[5].text != " " and len(j[5])<7:
           print("DP9: " + j[5][0].text)
           print("DP10: " + Amdtscraper(j[5][1][0][0][0][0][0]).text + " " + Amdtscraper2(j[5][1][0][0][0][0],1).text)
           print("DP11: " + Amdtscraper(j[5][1][0][0][1][0][0]).text + " " + Amdtscraper2(j[5][1][0][0][1][0],1).text)
        else:
           print("DP9: -")
           print("DP10: -")
           print("DP11: -")
        if j[6].text != " ":
           print("Notes" + j[6][0].attrib["title"].split("\n")[2].strip())
        osmxml.append(x)
        id-=1
        

        #print("DP4: " + j[4][0][0][0][0][0][0][4].text)
        #print("DP5: " + j[4][0][0][0][1][0][0][4].text)
      b+=1
      k+=1
  a+=1
  b=1
  print("\n")
  #x.append(ET.Element("nd",{"ref":waypointlist.index(y)}))


f.close()



osmxmltree = ET.ElementTree(element=osmxml)
ET.indent(osmxmltree, space="\t", level=0)
osmxmltree.write("output.osm")
print(waypointlist)





