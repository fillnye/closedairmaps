import xml.etree.ElementTree as ET

def Amdtscraper(x):
  try:
    if x[0].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[0]
    else:
        return x
  except IndexError:
        return x


id = 100000000
f = open("SP.xhtml", "r")
tree = ET.fromstring(f.read())
for i in tree[1][1][1][1][:-1]:
    print("id:" + str(id))
    print("Name:" +  Amdtscraper(i[0][0]).text)
    print("Long:" + Amdtscraper(i[1][0][0]).text)
    print("Lat:" + Amdtscraper(i[1][1][0]).text)
    try:
     print("FRA:" + Amdtscraper(i[3][0]).text)
    except IndexError:
     pass
    try:
     print("Notes:" + Amdtscraper(i[4][0][0]).text)
    except IndexError:
     print("Notes:None")
    id+=1
