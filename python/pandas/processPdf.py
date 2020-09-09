#!/usr/bin/python3.7
import tabula

def processCasesTable(index,filename):

    # Read pdf into list of DataFrame
    df = tabula.read_pdf(f"./data/{filename}", pages='1')

    conf=df[0]
    conf.drop([0,1,2,3],inplace=True)
    len(conf.columns)
    conf.columns=["ccaa","ct","c1","c14","c7","d14","d7"]

    ccaa = conf.iloc[:, 0]
    ccaa.columns=['ccaa']

    casos_t = conf.iloc[:, 1].str.replace(".","").astype(int)
    casos_1d = conf.iloc[:, 2].str.replace(".","").astype(int)

    conf["casos_t"]=casos_t
    conf["casos_1d"]=casos_1d

    c14 = conf.iloc[:, 3].str.split(" ",n=1,expand=True)
    casos_14d = c14[0].str.replace(".","").astype(int)
    iac_14d = c14[1].str.replace(",",".").astype(float)
    conf["casos_14d"]=casos_14d
    conf["iac_14d"]=iac_14d


    s14 = conf.iloc[:, 5].str.split(" ",n=1,expand=True)
    sintomas_14d = s14[0].str.replace(".","").astype(int)
    ias_14d = s14[1].str.replace(",",".").astype(float)
    conf["sintomas_14d"]=sintomas_14d
    conf["ias_14d"]=ias_14d

    conf["filename"]=filename
    conf["index"]=index
    print(conf)
    result = conf.to_json(orient="records")
    print(result)


if __name__ == '__main__':
    pdf=processCasesTable("203","Actualizacion_203_COVID-19.pdf")
