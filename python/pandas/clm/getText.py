from bs4 import BeautifulSoup
import urllib.request
import sys
import re
import json
import glob


PROVINCES = ["Toledo", "Ciudad Real", "Albacete", "Guadalajara", "Cuenca"]
HOSPITALS = ["Hospital de Toledo",  "Hospital de Talavera de la Reina", 
             "Hospital de Ciudad Real", "Hospital Mancha Centro", "Hospital de Puertollano", "Hospital de Tomelloso", "Hospital de Valdepeñas", "Hospital de Manzanares", 
             "Hospital de Guadalajara", 
             "Hospital de Albacete", "Hospital de Villarrobledo", "Hospital de Hellín",
             "Hospital de Cuenca"]


def parseNote(filename):
    f=open(filename,"r")
    html=f.read()
    soup = BeautifulSoup(html,features="html.parser")
    titleObj=soup.find("div", {"class": "even titulo"})
    title = titleObj.getText() if titleObj else ""
    #intro=soup.find("div", {"class": "even entradilla"}).getText()
    bodyObj=soup.find("div", {"class": "even contenido"})
    body = bodyObj.getText() if bodyObj else ""

    print(f"Title:{title }")
    m = re.search("Castilla-La Mancha.*(confirma|registra).*coronavirus|(número|nuevos).* contagios", title)

    if not m:
        print("No match!")
        return

    #get date from file name
    m=re.search(r"(\d+-\d+-\d+)-",filename)
    isodate = f"{m.group(1)}" if m else None


    data = {}
    print(body)
    print("------")
    body1 = re.sub(r'(\d)\.(\d)', r'\1\2', body)
    body2 = re.sub(r"COVID[-\d]*","covid",body1, flags=re.IGNORECASE)
    body3 = re.sub(r"\.",".\n",body2)
    body4 = re.sub(r"\n[\t ]+","\n",body3)
    
    replaceDict= { "á": "a",
                   "é": "e",
                   "í": "i",
                   "ó": "o",
                   "ú": "u"
    }
    for province in PROVINCES:
        replaceDict[province] = "#"+province.replace(" ","")

    body5 = multiple_replace(replaceDict, body4)

    tableType=None
    tableProvince=None


    sent = body5.split("\n")
    for line in sent:

        print(line)

        m = re.search(r"Recomendaciones", line)
        if m:
            print("# END DATA")
            break

        table = parseForType(line)
        if table:
            tableType = table
            tableProvince = None

        table = parseForProvinces(line)
        if table:
            tableProvince = table

        if tableType and tableProvince:
            ret = {**tableType, **tableProvince}
            print(json.dumps(ret, indent=4))
            tableType=None
            tableProvince=None

            #Transpose values
            type = ret.get("type")
            for province in PROVINCES + ["CLM"]:
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


    #print(json.dumps(record, indent=4))
    return record




    return None




def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 


def parseForType(para):

    table = {}
    m = re.search(r"provincia", para)
    table["provinces"] = True if m else False


    #casos
    m = re.search(r"confirmado (\d+) nuevos.*(casos|contagios)", para)
    if m:
        print(f"#1day, provinces:{table.get('provinces')}")
        table["type"]="cases_1d"
        table["CLM"]=m.group(1)

    m = re.search(r" (\d+) nuevos.*(casos|contagios).*confirmados", para)
    if m:
        print(f"#1day, provinces:{table.get('provinces')}")
        table["type"]="cases_1d"
        table["CLM"]=m.group(1)

    m = re.search(r"acumulado.*casos.* (\d+)\.", para)
    if m:
        print(f"#total, provinces:{table.get('provinces')}")
        table["type"]="cases_total"
        table["CLM"]=m.group(1)

    m = re.search(r"casos.*acumulado.* (\d+)\.", para)
    if m:
        print(f"#total, provinces:{table.get('provinces')}")
        table["type"]="cases_total"
        table["CLM"]=m.group(1)


    m = re.search(r"hospital.*convencional.* (\d+)\.", para)
    if m:
        print(f"#pacientes, provinces:{table.get('provinces')}")
        table["type"]="hospital_current"
        table["CLM"]=m.group(1)

    m = re.search(r"convencional.*hospital.*(\d+)\.", para)
    if m:
        print(f"#pacientes, provinces:{table.get('provinces')}")
        table["type"]="hospital_current"
        table["CLM"]=m.group(1)

    m = re.search(r" (\d+) .*hospital.*convencional(\.|,)", para)
    if m:
        print(f"#pacientes, provinces:{table.get('provinces')}")
        table["type"]="hospital_current"
        table["CLM"]=m.group(1)


    m = re.search(r" (\d+).*Intensivos.*\.", para)
    if m:
        print(f"#uci, provinces:{table.get('provinces')}")
        table["type"]="icu_current"
        table["CLM"]=m.group(1)

    m = re.search(r"Intensivos.* (\d+)\.", para)
    if m:
        print(f"#uci, provinces:{table.get('provinces')}")
        table["type"]="icu_current"
        table["CLM"]=m.group(1)



    m = re.search(r"24 horas.*(\d+).*fallecimiento.*, ", para)
    if m:
        print(f"#death 1d, provinces:{table.get('provinces')}")
        table["type"]="death_1d"
        table["CLM"]=m.group(1)

    m = re.search(r"fin de semana.*(\d+).*fallecimiento.*, ", para)
    if m:
        print(f"#death 1d, provinces:{table.get('provinces')}")
        table["type"]="death_1d"
        table["CLM"]=m.group(1)

    m = re.search(r"fallecimientos.*inicio.* a (\d+)\.", para)
    if m:
        print(f"#death total, provinces:{table.get('provinces')}")
        table["type"]="death_total"
        table["CLM"]=m.group(1)

    m = re.search(r"fallecidos.*inicio.* es (\d+)\.", para)
    if m:
        print(f"#death total, provinces:{table.get('provinces')}")
        table["type"]="death_total"
        table["CLM"]=m.group(1)


    if not table.get("type"):
        return None

    return table

def parseForProvinces(para):

    table = {}

    m = re.search(r"provincia", para)
    if not m:
        return None

    # Get provincias
    for province in PROVINCES:
        m = re.search(getTag(province)+r"[a-zA-Z ]+(\d+)[a-z ]*[,.y(]", para)
        if m:
            match = m.group(0)
            value = m.group(1)
            print(f"match '{match}', Province:{province}, value:{value}")
            table[province]=value
            continue

        m = re.search(r"[,y] (\d+)[a-zA-z ]+"+getTag(province)+"[ ,.y(]", para)
        if m:
            match = m.group(0)
            value = m.group(1)
            print(f"match '{match}', Province:{province}, value:{value}")
            table[province]=value            
        
    return table


def getTag(text):
    return "#"+text.replace(" ","")


def parseByDate(date):
    filenameList = glob.glob(f"./notas/{date}*.html")

    table = []

    for filename in filenameList:
        ret = parseNote(filename) 
        if ret:
            table = table + ret

    print(json.dumps(table, indent=4))
    return table

if __name__ == '__main__':

    #getLastPages()

    #filename = sys.argv[1]
    #parseNote(filename)

    date = sys.argv[1]
    parseByDate(date)


    #date = sys.argv[1]
    #getNotesFromDay(date)
