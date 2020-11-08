#!/usr/bin/python3
import tabula
import sys
import json
import getTable
from tableMap import getTableMap, getTableCols

def processBedsTable(filename):

    # Get Index & TableMap
    index = getTable.getIdFromFilename(filename)
    tableName = "beds"
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

    #colInt   = [ "hospital_cur", "icu_cur" ]
    #colFloat = [ "hospital_ratio", "icu_ratio" ]

    #Convert to Int
    getTable.cols2int(conf,colInt)
    #Convert to Float
    getTable.cols2float(conf,colFloat)


    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result




if __name__ == '__main__':

    pdf=processBedsTable(sys.argv[1])
