#!/usr/bin/python3
import tabula
import sys
import json
import getTable
from tableMap import getTableMap, getTableCols

def processHospitalTable(filename):


    # Get Index & TableMap
    index = getTable.getIdFromFilename(filename)
    tableName = "hospital"
    tableMap = getTableMap(index,tableName)
    colInt, colFloat = getTableCols(tableName)

    # Read pdf into list of DataFrame
    if tableMap.get("template"):
        print(f"Using template.")
        df = tabula.read_pdf_with_template(f"./data/{filename}", f"./templates/{tableMap['template']}")
    else:
        df = tabula.read_pdf(f"./data/{filename}", pages=tableMap["page"])

    # Select table in page
    conf = getTable.checkSize(df,18,len(tableMap["colNames"]))

    # Remove header
    getTable.rmHeader(conf)

    # Rename columns
    conf.columns=tableMap["colNames"]

    #print(conf)

    if ("hospital_g1" in tableMap["colNames"]):
        hospital = conf["hospital_g1"].str.split(" ",n=1,expand=True)
        conf["hospital_total"]=hospital[0]
        conf["hospital_7d"]   =hospital[1]

    if ("icu_g1" in tableMap["colNames"]):
        icu = conf["icu_g1"].str.split(" ",n=1,expand=True)
        conf["icu_total"]=icu[0]
        conf["icu_7d"]   =icu[1]


    #colInt = [ "hospital_total", "hospital_7d", "icu_total", "icu_7d", "death_total", "death_7d" ]
    #Convert to Int
    getTable.cols2int(conf,colInt)
    #Convert to Float
    getTable.cols2float(conf,colFloat)


    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result




if __name__ == '__main__':

    pdf=processHospitalTable(sys.argv[1])
