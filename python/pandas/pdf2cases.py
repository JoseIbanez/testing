#!/usr/bin/python3.7
import tabula
import sys
import json

def processCasesTable(filename):

    # Read pdf into list of DataFrame
    df = tabula.read_pdf(f"./data/{filename}", pages='1')

    conf=df[0]
    col0 = conf.columns[0]
    print("col0:"+col0)
    if 'SECRETARÍA' in col0:
        conf=df[1]
    print(conf.columns)


    conf.drop([0,1,2,3],inplace=True)
    conf.columns=["region_name","ct","c1","c14","c7","d14","d7"]

    ccaa = conf.iloc[:, 0]
    ccaa.columns=['region_name']

    casos_t = conf.iloc[:, 1].str.replace(".","").astype(int)
    casos_1d = conf.iloc[:, 2].str.replace(".","").astype(int)

    conf["cases_total"]=casos_t
    conf["cases_1day"]=casos_1d

    c14 = conf.iloc[:, 3].str.split(" ",n=1,expand=True)
    casos_14d = c14[0].str.replace(".","").astype(int)
    iac_14d = c14[1].str.replace(",",".").astype(float)
    conf["cases_14d"]=casos_14d
    conf["cases_14d_ai"]=iac_14d


    s14 = conf.iloc[:, 5].str.split(" ",n=1,expand=True)
    sintomas_14d = s14[0].str.replace(".","").astype(int)
    ias_14d = s14[1].str.replace(",",".").astype(float)
    conf["symptoms_14d"]=sintomas_14d
    conf["symptoms_14d_ai"]=ias_14d

    conf["filename"]=filename
    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result

if __name__ == '__main__':

    pdf=processCasesTable(sys.argv[1])
