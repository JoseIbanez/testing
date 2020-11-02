#!/usr/bin/python3
import tabula
import sys
import json
import getTable
from tableMap import getTableMap


def processCasesTable(filename):

    # Get Index & TableMap
    index = getTable.getIdFromFilename(filename)
    tableName = "cases"
    tableMap = getTableMap(index,tableName)

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
    #conf.columns=["region_name","cases_total","cases_1d","cases_g14","cases_g7","d14","d7"]

    print(conf)

    if ("cases_g14" in tableMap["colNames"]):
        c14 = conf["cases_g14"].str.split(" ",n=1,expand=True)
        conf["cases_14d"]=c14[0]
        conf["cases_14d_ai"]=c14[1]

    if ("cases_g7" in tableMap["colNames"]):
        c7 = conf["cases_g7"].str.split(" ",n=1,expand=True)
        conf["cases_7d"]=c7[0]
        conf["cases_7d_ai"]=c7[1]

    if ("symptoms_g14" in tableMap["colNames"]):
        s14 = conf["symptoms_g14"].str.split(" ",n=1,expand=True)
        conf["symptoms_14d"]=s14[0]
        conf["symptoms_14d_ai"]=s14[1]

    if ("symptoms_g7" in tableMap["colNames"]):
        s7 = conf["symptoms_g7"].str.split(" ",n=1,expand=True)
        conf["symptoms_7d"]=s7[0]
        conf["symptoms_7d_ai"]=s7[1]


    colInt = [ "cases_total", "cases_1day", "cases_14d", "cases_7d", "symptoms_14d", "symptoms_7d" ]
    #Convert to Int
    getTable.cols2int(conf,colInt)

    colFloat = [ "cases_14d_ai", "cases_7d_ai", "symptoms_14d_ai", "symptoms_7d_ai" ]
    #Convert to Float
    getTable.cols2float(conf,colFloat)


    #conf["filename"]=filename
    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result

if __name__ == '__main__':

    pdf=processCasesTable(sys.argv[1])
