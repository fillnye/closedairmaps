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
f = open("NAV.xhtml", "r")
tree = ET.fromstring(f.read())
for i in tree[1][1][1][1][1]:
    print("id:" + str(id))
    print("Name:" +  i[0][0][0].text)
    print("Type:NAVAID")
    if(i[0][1][1].tail!=None):
        if(i[0][1][1].tail=="/DME"):
            print("navaid:" + i[0][1][0].text + i[0][1][1].tail)
        else:
            print("navaid:" + i[0][1][0].text)
    else:
        print("navaid:" + i[0][1].text)
    print("ID:" +  i[1][0].text)
    if len(i[2])==1:
        print("frequency:" + i[2][0][0].text)
    elif len(i[2][0])==4:
        print("frequency:" + i[2][0][0].text)
        print("channel:" + i[2][1][0].text)
    else:
        print("channel:" + i[2][0][0].text)
        print("frequency:" + i[2][1][0].text)
    print("Long:" + Amdtscraper(i[4][0][0]).text)
    print("Lat:" + Amdtscraper(i[4][1][0]).text)
    try:
     print("Ele:" + Amdtscraper(i[5][0][0]).text + " FT")
    except IndexError:
     pass
    try:
     s = Amdtscraper(i[7][0][0]).text
     for j in Amdtscraper(i[7][0][0]):
        if j.tail != None:
            s += "\n" + j.tail
     print("Notes:" + s)
    except IndexError:
     pass
    id-=1
    
