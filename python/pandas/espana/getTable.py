#!/usr/bin/python3
import sys
import json
import re
import pandas as pd 
from tableMap import getTableMap


def getIdFromFilename(filename):

    regex = re.compile(r"Actualizaci.n_(\d+)_COVID.*")
    result = regex.match(filename)
    if not result:
        raise RuntimeError("No index number in filename")

    index = int(result.group(1))

    return index



def checkSize(df,rows,cols):
    """
    Check size of table
    If few rows, next table in same page
    If wrong cols, then stop
    """

    numberTables=len(df)

    for i in range(0,numberTables):
        conf=df[i]
        print(f"table:{i}/{numberTables}, shape:{conf.shape}")
        print(conf)
        if (conf.shape[0] >= rows):
            break

    if (conf.shape[1] != cols):
        raise RuntimeError("Table format does match!")

    return conf



def cols2int(conf,colInt):

    for colName in colInt:
        if (colName in conf.columns):
            print(colName)
            conf[colName] = conf[colName].str.replace("-","0")
            conf[colName] = conf[colName].str.replace(".","").astype(int)

    return


def cols2float(conf,colFloat):

    for colName in colFloat:
        if (colName in conf.columns):
            print(colName)
            #if isinstance(conf[colName],str):
            conf[colName] = conf[colName].str.replace("%","")
            conf[colName] = conf[colName].str.replace(",",".").astype(float)

    return


def rmHeader(conf):

    n_row, n_col = conf.shape
    n_header = None
    #title = [""] * n_col

    #print(conf)

    for i in range(0,n_row):
        print(conf.iloc[i][0])
        if ('Andalucía' in str(conf.iloc[i][0])):
            n_header = i
            break

        #for l in range(0, n_col):
        #    cel = conf.iloc[i][l]
        #    if cel:
        #        title[l] += cel
            
    #if (not n_header):
    #    raise RuntimeError("Headers not found!")

    if (n_header):
        #print(f"n_header {n_header}")
        #print(title)
        conf.drop(range(0,n_header),inplace=True)
        #print(conf)


def loadFromFile(filename):
    df = pd.read_json ("./data/t3.json")
    print(df)
    return df



def save2file(df):
    table = df.to_json()
    with open("./data/t3.json", "w") as file:  # Use file to refer to the file object
        file.write(table)

    return 


if __name__ == '__main__':

    #pdf=processHospitalTable(sys.argv[1])
    checkTable()