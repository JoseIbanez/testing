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
        format = 100

    if conf_len == 7:
        format = 185
    
    

    if format == 100:
        print(f"Format: {format}")
        print(conf)    

        conf.drop([0,1],inplace=True)
        conf.columns=["region_name","ct","c1","inc1","ia14"]

        conf["cases_total"]=conf["ct"].str.replace(".","").astype(int)
        conf["cases_1day"]=conf["c1"].str.replace(".","").astype(int)

        conf["cases_14d_ai"]=conf["ia14"].str.replace(",",".").astype(float)



    if format == 185:
        print(f"Format: {format}")
        print(conf)
        conf.drop([0,1,2,3],inplace=True)
        conf.columns=["region_name","ct","c1","c14","c7","d14","d7"]

        print(conf)        

        #ccaa = conf.iloc[:, 0]
        #ccaa.columns=['region_name']

        casos_t = conf.iloc[:, 1].str.replace(".","").astype(int)
        casos_1d = conf.iloc[:, 2].str.replace(".","").str.replace("-","0").astype(int)

        conf["cases_total"]=casos_t
        conf["cases_1day"]=casos_1d

        c14 = conf.iloc[:, 3].str.split(" ",n=1,expand=True)
        casos_14d = c14[0].str.replace(".","").astype(int)
        iac_14d = c14[1].str.replace(",",".").astype(float)
        conf["cases_14d"]=casos_14d
        conf["cases_14d_ai"]=iac_14d


        c7 = conf.iloc[:, 4].str.split(" ",n=1,expand=True)
        casos_7d = c7[0].str.replace(".","").astype(int)
        iac_7d = c7[1].str.replace(",",".").astype(float)
        conf["cases_7d"]=casos_7d
        conf["cases_7d_ai"]=iac_7d


        s14 = conf.iloc[:, 5].str.split(" ",n=1,expand=True)
        sintomas_14d = s14[0].str.replace(".","").astype(int)
        ias_14d = s14[1].str.replace(",",".").astype(float)
        conf["symptoms_14d"]=sintomas_14d
        conf["symptoms_14d_ai"]=ias_14d

        s7 = conf.iloc[:, 6].str.split(" ",n=1,expand=True)
        sintomas_7d = s7[0].str.replace(".","").astype(int)
        ias_7d = s7[1].str.replace(",",".").astype(float)
        conf["symptoms_7d"]=sintomas_7d
        conf["symptoms_7d_ai"]=ias_7d


    #conf["filename"]=filename
    print(conf)
    result = json.loads(conf.to_json(orient="records"))
    #print(result)
    return result

if __name__ == '__main__':

    pdf=processCasesTable(sys.argv[1])
