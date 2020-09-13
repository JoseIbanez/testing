#!/usr/bin/python3.7

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import re
import json

def pdfToken(filename):

    fp = open(f"./data/{filename}", 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document.
    #for page in PDFPage.get_pages(fp):
    #    interpreter.process_page(page)
    #    data =  retstr.getvalue()

    # Proccess page 1
    page = next(PDFPage.get_pages(fp),None)    
    interpreter.process_page(page)
    data =  retstr.getvalue()

    index = None
    date = None
    lines = data.split("\n")
    regex = re.compile(r"Actualizaci.n n. (\d+). Enfermedad por el coronavirus .COVID-19.\. (\d+\.\d+\.\d+) .datos consolidados ")
    for line in lines:
        result = regex.match(line)
        if not result:
            continue
        print(line)
        print(result)
        index = result.group(1)
        date = result.group(2)
        print(f"Detected token, index:{index} with date:{date}")
        break

    if not date:
        raise RuntimeError("Token not found in pdf. No index, no date!")

    result = re.match(r"(\d+)\.(\d+)\.(\d+)",date)
    isodate=f"{result.group(3)}-{result.group(2)}-{result.group(1)}"
    print(f"Result, index:{index}, isodate:{isodate}.")

    return {
        "index": index,
        "isodate": isodate
    }

    #print(data)

if __name__ == '__main__':

    ret = pdfToken(sys.argv[1]) 
    print(json.dumps(ret))

    #with open(f"./data/task-{index}.date.json", "w") as f:
    #    f.write("Purchase Amount: %s" % TotalAmount)
