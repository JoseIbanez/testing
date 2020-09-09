import urllib.request



def getGovPdf(index):

    baseurl="https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/"
    filename = f"Actualizacion_{index}_COVID-19.pdf"
    url = baseurl + filename

    print (url)

    urllib.request.urlretrieve(url, f"./data/{filename}")
    return filename 

    
    #raise RuntimeError("Download failed!")



if __name__ == '__main__':
    pdf=getGovPdf(100)
