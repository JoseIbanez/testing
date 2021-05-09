#!/usr/bin/python3.7

import sys
import json
from tableMap import getTableMap, getTableCols


REGIONS = [
  {"id":"ES", "name":"ESPAÑA", "isoname":"España"},
  {"id":"ES", "name":"TOTAL", "isoname":"España"},
  {"id":"ES", "name":"Total general", "isoname":"España"},  
  {"id":"AN", "name":"Andalucía", "isoname":"Andalucía"},
  {"id":"AR", "name":"Aragón", "isoname":"Aragón"},
  {"id":"AS", "name":"Asturias"},
  {"id":"IB", "name":"Baleares","isoname":"Illes Balears"},
  {"id":"IB", "name":"Islas Baleares","isoname":"Illes Balears"},
  {"id":"CN", "name":"Canarias", "isoname":"Canarias"},
  {"id":"CN", "name":"Islas Canarias", "isoname":"Canarias"},
  {"id":"CB", "name":"Cantabria"},
  {"id":"CM", "name":"Castilla La Mancha"},
  {"id":"CL", "name":"Castilla y León","isoname":"Castilla y León"},
  {"id":"CT", "name":"Cataluña"},
  {"id":"CE", "name":"Ceuta"},
  {"id":"VC", "name":"C. Valenciana"},
  {"id":"VC", "name":"C Valenciana"},
  {"id":"EX", "name":"Extremadura"},
  {"id":"GA", "name":"Galicia"}, 
  {"id":"MD", "name":"Madrid"},
  {"id":"ML", "name":"Melilla"},
  {"id":"MC", "name":"Murcia"},
  {"id":"NC", "name":"Navarra"},
  {"id":"PV", "name":"País Vasco"},
  {"id":"RI", "name":"La Rioja"}
]


def searchLocation(in_name):


    id = None
    name = in_name.replace('*','')

    for region in REGIONS:

        if name == region["name"]:
            id = region["id"]
            #print(f"Name: {name}, Id:{id}")
            break

    if not id:
        raise RuntimeError(f"Location: {name}, ISO Id not found")


    return id    


def getConfirmedCases(index,cases,date):

    result = []
    for case in cases:
        item={}
        item["index"]=index
        item["region_name"]=case["region_name"]
        item["region_iso"]=searchLocation(case["region_name"])
        item["date"]=date["isodate"]
        item["cases_total"]      = case["cases_total"]  
        item["cases_1day"]       = case["cases_1day"]   
        item["cases_14d"]        = case.get("cases_14d")
        item["cases_14d_ai"]     = case["cases_14d_ai"]  
        item["cases_7d"]        = case.get("cases_7d")
        item["cases_7d_ai"]     = case.get("cases_7d_ai")  
        item["symptoms_14d"]     = case.get("symptoms_14d")
        item["symptoms_14d_ai"]  = case.get("symptoms_14d_ai")  
        item["symptoms_7d"]     = case.get("symptoms_7d")
        item["symptoms_7d_ai"]  = case.get("symptoms_7d_ai")  

        item["id"] = f"{index}.{item['region_iso']}"

        #print(json.dumps(item))
        result.append(item)

    return result


def prepareBedDict(beds):
    tableName = "beds"
    colInt, colFloat = getTableCols(tableName)

    bedDict = {}
    for b in beds:
        region= searchLocation(b["region_name"])
        bedDict[region]={}
        for c in colInt + colFloat:
            #print(f"{region} {c}")
            bedDict[region][c] = b.get(c)

    return bedDict        


def getHospital(index,hospital,beds,date):

    bedDict = prepareBedDict(beds)


    result = []
    for h in hospital:
        item={}
        item["index"]=index
        region=searchLocation(h["region_name"])
        item["region_iso"]=region
        item["region_name"]= h["region_name"]
        item["date"]=date["isodate"]
        item["id"] = f"{index}.{region}"


        count_h = 0
        count_b = 0

        tableName = "hospital"
        colInt, colFloat = getTableCols(tableName)
        for c in colInt + colFloat:
            item[c] = h.get(c)
            count_h += 1 if not item[c] is None  else 0

        tableName = "beds"
        colInt, colFloat = getTableCols(tableName)
        for c in colInt + colFloat:
            item[c] = bedDict[region][c]
            count_b += 1 if not item[c] is None else 0

        print(f"{item['id']}, hospital:{count_h}, beds:{count_b}")
        #print(json.dumps(item))
        result.append(item)

    return result



if __name__ == '__main__':

    index = sys.argv[1]

    date = None
    cases = None

    with open(f"./data/task-{index}.date.json", 'r') as file:
        date = json.loads(file.read())

    #with open(f"./data/task-{index}.cases.json", 'r') as file:
    #    cases = json.loads(file.read())

    #t_cases = getConfirmedCases(index,cases,date)

    with open(f"./data/task-{index}.hospital.json", 'r') as file:
        hospital = json.loads(file.read())

    with open(f"./data/task-{index}.beds.json", 'r') as file:
        beds = json.loads(file.read())

    t_hospital = getHospital(index,hospital,beds,date)
