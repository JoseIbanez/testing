#!/usr/bin/python3
import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer



def parse_obj(lt_objs, text, pos):


    # loop over the object list
    for obj in lt_objs:

        if isinstance(obj, pdfminer.layout.LTTextLine):
            #print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))

            for idx,item in enumerate(text):

                if item in obj.get_text():
                    #print(obj.get_text())
                    #print(obj.bbox)            
                    pos[idx]={"box":obj.bbox,"token":item,"text":obj.get_text().replace('\n', '_')}


        # if it's a textbox, also recurse
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            parse_obj(obj._objs, text, pos)

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs, text, pos)

def pdfSearch(filename, nPage, text):

    # Open a PDF file.
    fp = open(filename, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pos = {}
    i = 1
    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        #print(f"page: {page}")
        if i == nPage:
            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            #print(f"page: {page.mediabox}")
            pos["mediabox"] = page.mediabox
            parse_obj(layout._objs, text, pos)
        i += 1
  
    return pos


def pdfSearchPage(filename,token):

    for nPage in range(1,10):
        print(f"Looking for {token}, Page:{nPage}")
        pos = pdfSearch(filename,nPage,[token])
        if pos.get(0):
            print(f"Found '{token}' in page {nPage}")
            print(pos)
            return nPage
        
    return None


def pdfHospitalCoordinates(filename):

    nPage = pdfSearchPage(filename, "Tabla 2.")
    tokens = ["Tabla 2.","CCAA","ESPAÑA","últimos 7 días"]

    pos = pdfSearch(filename, nPage, tokens)
    print("Hospital")
    x1 = pos[0]["box"][0] - 10
    x2 = pos[3]["box"][2]
    y1 = pos["mediabox"][3]-pos[1]["box"][3]
    y2 = pos["mediabox"][3]-pos[2]["box"][1]
    pos["area"] = (y1,x1,y2,x2)
    pos["page"] = nPage
    print(pos)
    print(f"Coordinates: y1:{y1}, x1:{x1}, y2:{y2}, x2:{x2}")
    print("---")
    return pos


def pdfBedCoordinates(filename):

    nPage = pdfSearchPage(filename, "Tabla 3.")
    tokens = ["Tabla 3.","CCAA","ESPAÑA","Altas"]

    pos = pdfSearch(filename, nPage, tokens)
    print("Beds")
    x1 = pos[0]["box"][0] - 10
    x2 = pos[3]["box"][2]
    y1 = pos["mediabox"][3]-pos[1]["box"][3]
    y2 = pos["mediabox"][3]-pos[2]["box"][1]
    pos["area"] = (y1,x1,y2,x2)
    pos["page"] = nPage
    print(pos)
    print(f"Coordinates: y1:{y1}, x1:{x1}, y2:{y2}, x2:{x2}")
    print("---")
    return pos



if __name__ == '__main__':

    filename = sys.argv[1]

    #pos = pdfSearchPage(filename,"Tabla 2.")

    #print("------")

    pos = pdfHospitalCoordinates(filename)
    pos = pdfBedCoordinates(filename)


  