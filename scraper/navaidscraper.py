import xml.etree.ElementTree as ET

def Amdtscraper(x):
  try:
    if x[0].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[0]
    else:
        return x
  except IndexError:
        return x


id = 120000000
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
    id+=1
    
