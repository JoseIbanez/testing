from bs4 import BeautifulSoup
import urllib.request
import sys
import re
import json

PROVINCES = ["Toledo", "Ciudad Real", "Albacete", "Guadalajara", "Cuenca"]


def parseNote(filename):
    f=open(filename,"r")
    html=f.read()
    soup = BeautifulSoup(html,features="html.parser")
    title=soup.find("div", {"class": "even titulo"}).getText()
    intro=soup.find("div", {"class": "even entradilla"}).getText()
    body=soup.find("div", {"class": "even contenido"}).getText()

    print(f"Title:{title}")
    m = re.search("Castilla-La Mancha.*confirma.*coronavirus", title)

    if not m:
        print("No match!")
        return

    #get date
    m=re.search(r"(\d+-\d+-\d+)-",filename)
    if m:
        isodate = f"{m.group(1)}"
    else:
        isodate = None

    #print(intro)
    #print(body)

    data = {}

    prePara = None
    paras = body.split("\n")
    for para in paras:
        #print(para)

        if len(para) < 10:
            continue

        # if pending paragraph        
        if prePara:
            #print(f"pre:'{prePara}' para:'{para}'")
            ret = parseParagraph(prePara+" "+para)
        else:
            ret = parseParagraph(para)

        # if not match
        if not ret:
            prePara = None
            continue    

        # if not provinces, only 1st part of paragraph 
        if ret and not ret.get("provinces"):
            prePara = para
            continue

        # full match
        prePara = None
        #print(json.dumps(ret))

        type = ret.get("type")
        for province in PROVINCES:
            value = ret.get(province)

            if not data.get(province):
                data[province]={}
            data[province][type]=value

    record = []
    for province in data:
        item = data.get(province)
        item['region_name'] = province
        item['date'] = isodate
        item['id'] = f"{item['date']}.{item['region_name']}"
        record.append(item)


    print(json.dumps(record))

def parseParagraph(paraIn):

    table = {}

    m = re.search(r"Por provincias|en la provincia", paraIn)
    if m:
        table["provinces"] = True
    else:
        table["provinces"] = False



    # Remove . from numbers, From 12.000 to 12000
    para = re.sub(r'(\d)\.(\d)', r'\1\2', paraIn)
    print(">"+para+"<")


    #casos
    m = re.search(r"confirmado (\d+) nuevos contagios en las últimas 24 horas", para)
    if m:
        print(f"#1day, provinces:{table.get('provinces')}")
        table["type"]="cases_1d"
        table["CLM"]=m.group(1)

    m = re.search(r"total de casos acumulados.* es (\d+)\.", para)
    if m:
        print(f"#total, provinces:{table.get('provinces')}")
        table["type"]="cases_total"
        table["CLM"]=m.group(1)

    m = re.search(r"hospitalizados.*convencional es (\d+)\.", para)
    if m:
        print(f"#pacientes, provinces:{table.get('provinces')}")
        table["type"]="hospital_current"
        table["CLM"]=m.group(1)

    m = re.search(r" (\d+).*Intensivos.*\.", para)
    if m:
        print(f"#uci, provinces:{table.get('provinces')}")
        table["type"]="icu_current"
        table["CLM"]=m.group(1)

    m = re.search(r"24 horas.*(\d+).*fallecimientos.*, ", para)
    if m:
        print(f"#death 1d, provinces:{table.get('provinces')}")
        table["type"]="death_1d"
        table["CLM"]=m.group(1)

    m = re.search(r"fallecimientos.*inicio.* a (\d+)\.", para)
    if m:
        print(f"#death total, provinces:{table.get('provinces')}")
        table["type"]="death_total"
        table["CLM"]=m.group(1)



    if not table.get("type"):
        return None

    if not table.get("provinces"):
        return table


    # Get provincias
    for province in PROVINCES:
        m = re.search(province+r"[a-zA-Z ]+(\d+)[a-z ]*[,.y(]", para)
        if m:
            match = m.group(0)
            value = m.group(1)
            print(f"match '{match}', Province:{province}, value:{value}")
            table[province]=value
            continue

        m = re.search(r"[,y] (\d+)[a-zA-z ]+"+province+"[ ,.y(]", para)
        if m:
            match = m.group(0)
            value = m.group(1)
            print(f"match '{match}', Province:{province}, value:{value}")
            table[province]=value            
        

    print(json.dumps(table))
    return table

if __name__ == '__main__':

    #getLastPages()

    filename = sys.argv[1]
    parseNote(filename)

    #date = sys.argv[1]
    #getNotesFromDay(date)
