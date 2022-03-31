import requests
import xml.etree.ElementTree as ET
def convertTODecimal(y, x):
    xneg = 1
    yneg = 1
    if(x[len(x)-1]=='W'):
        xneg=-1
    if(y[len(y)-1]=='S'):
        yneg=-1
    return [round(int(y[0:2])+int(y[2:4])/60.0+float(y[4:(len(y)-1)])/3600.0*yneg,11),round((int(x[0:3])+int(x[3:5])/60.0+float(x[5:(len(x)-1)])/3600)*xneg,11)]


def Amdtscraper(x):
  try:
    if x[0].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[0]
    else:
        return x
  except IndexError:
        return x

def Amdtscraper2(x,index):
  i = index*2
  try:
    if x[index].tag=="{http://www.w3.org/1999/xhtml}ins" or x.tag=="{http://www.w3.org/1999/xhtml}ins":
        return x[index][0]
    else:
        return x[i]
  except IndexError:
        return x[i]


#r = requests.get('https://www.aurora.nats.co.uk/htmlAIP/Publications/2022-02-24-AIRAC/html/eAIP/EG-ENR-3.3-en-GB.html')
f = open("ENR.xhtml", "r")
tree = ET.fromstring(f.read())
a = 1
b = 1


for i in tree[1][1][1:]:
  for j in i[2][1:]:
      if Amdtscraper(j[0]).text == "∆" or j[0].text == " " or Amdtscraper(j[0]).text == "▲":
       if j[1][0].tag == "{http://www.w3.org/1999/xhtml}strong":
        print("Type: NAVAID")
        print("Name: " + j[1][0][0].text)
       else:
        print("Type: Waypoint")
        print("Name:" + j[1][0].text)
       if Amdtscraper(j[0]).text == "▲":
        print("flyover=true")
       #print("Coord 1 " + j[2][0].text)
       #print("Coord 2 " + j[2][2].text)
       if j[4].text != " ":
           print("Notes: " + j[4][0].attrib["title"].split("\n")[1].strip())
      elif j[0][0].text!="(RNAV)":
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

        #print("DP4: " + j[4][0][0][0][0][0][0][4].text)
        #print("DP5: " + j[4][0][0][0][1][0][0][4].text)
      b+=1
  a+=1
  b=1
  print("\n")


f.close()
#if rowindex%2 == 0:
#        print("Type Leg")
#        print("RNP: " + tree[1][1][1][tableindex][2][rowindex][0][0].text)
#        print("DP1: " + tree[1][1][1][tableindex][2][rowindex][1][0][0][0][0][0][0][0].text)
#        print("DP2: " + tree[1][1][1][tableindex][2][rowindex][1][0][0][0][1][0][0][0].text)
#        print("DP3: " + tree[1][1][1][tableindex][2][rowindex][2][0][0].text)
#        print("DP4: " + tree[1][1][1][tableindex][2][rowindex][4][0][0][0][0][0][0][4].text)
#        print("DP5: " + tree[1][1][1][tableindex][2][rowindex][4][0][0][0][1][0][0][4].text)
#elif tree[1][1][1][tableindex][2][rowindex][1][0].tag == "{http://www.w3.org/1999/xhtml}strong":
#        print("Type: NAVAID")
#        print("Name: " + tree[1][1][1][tableindex][2][rowindex][1][0][0].text)
#        print("Coord 1 " + tree[1][1][1][tableindex][2][rowindex][2][0].text)
#        print("Coord 2 " + tree[1][1][1][tableindex][2][rowindex][2][2].text)
#else:
#        print("Type: Waypoint")
#        print(tree[1][1][1][tableindex][2][rowindex][1][0].text)
#        print("Coord 1 " + tree[1][1][1][tableindex][2][rowindex][2][0].text)
#        print("Coord 2 " + tree[1][1][1][tableindex][2][rowindex][2][2].text)
