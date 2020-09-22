#!/usr/bin/python3
import tabula
import sys
import json

def processHospitalTable(filename):

    # Read pdf into list of DataFrame
    df = tabula.read_pdf(f"./data/{filename}", pages='2')

    conf=df[0]
    col0 = conf.columns[0]
    print("col0:"+col0)
    if 'SECRETARÍA' in col0 or 'SECRETARIA' in col0:
        conf=df[1]

    conf_len = len(conf.columns)
    row_len = len(conf.index)
    print(f"len: {conf_len}, rows: {row_len}")

    if row_len < 20:
        conf=df[1]
        conf_len = len(conf.columns)
        row_len = len(conf.index)
        print(f"len: {conf_len}, rows: {row_len}")


    print(conf.columns)

    format = 0
    if conf_len == 5:
        format = 5    

    if conf_len == 7:
        format = 7    


    if format == 5:
        print(f"Format: {format}")
        print(conf)    

        conf.drop([0,1,2],inplace=True)
        conf.columns=["region_name","hospital","icu","dt","d7"]


        hospital = conf["hospital"].str.split(" ",n=1,expand=True)
        conf["hospital_total"]=hospital[0].str.replace(".","").astype(int)
        conf["hospital_7d"] =hospital[1].str.replace(".","").astype(int)

        icu = conf["icu"].str.split(" ",n=1,expand=True)
        conf["icu_total"]=icu[0].str.replace(".","").astype(int)
        conf["icu_7d"] =icu[1].str.replace(".","").astype(int)

        conf["death_total"]=conf["dt"].str.replace(".","").astype(int)
        conf["death_7d"]=conf["d7"].str.replace(".","").astype(int)


    if format == 7:
        print(f"Format: {format}")
        print(conf)    

        conf.drop([0,1,2],inplace=True)
        conf.columns=["region_name","hospital","icu","dt","d7","pcr_cc","pcr_total"]


        hospital = conf["hospital"].str.split(" ",n=1,expand=True)
        conf["hospital_total"]=hospital[0].str.replace(".","").astype(int)
        conf["hospital_7d"] =hospital[1].str.replace(".","").astype(int)

        icu = conf["icu"].str.split(" ",n=1,expand=True)
        conf["icu_total"]=icu[0].str.replace(".","").astype(int)
        conf["icu_7d"] =icu[1].str.replace(".","").astype(int)

        conf["death_total"]=conf["dt"].str.replace(".","").astype(int)
        conf["death_7d"]=conf["d7"].str.replace(".","").astype(int)


    if format == 0:
        raise RuntimeError("Table format not detected!")


    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result

if __name__ == '__main__':

    pdf=processHospitalTable(sys.argv[1])
