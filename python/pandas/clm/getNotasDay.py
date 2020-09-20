from bs4 import BeautifulSoup
import urllib.request
import sys

LAST_PAGES = 10


def getLastPages():

    for index in range(0,LAST_PAGES):
        print(index)
        url = f"https://sanidad.castillalamancha.es/ciudadanos/enfermedades-infecciosas/coronavirus/notas-prensa?page={index}"
        urllib.request.urlretrieve(url, f"./notas/notas-prensa-{index}.html")


def getNotesFromDay(date):

    for index in range(0,LAST_PAGES):
        page = f"./notas/notas-prensa-{index}.html"
        getNotesFromPage(page,date)


def getNotesFromPage(page, reqDate = None):

    f=open(page,"r")
    html=f.read()
    soup = BeautifulSoup(html,features="html.parser")
    noteList = soup.find("div", {"class": "view-content"}).findAll("div",{"class":"group-right"})

    #print(noteList)

    for note in noteList:
        #print(note)

        date=note.find("span").getText().split("/")
        isodate=f"{date[2]}-{date[1]}-{date[0]}"

        print(f"{isodate}")

        if reqDate and reqDate != isodate:
            continue

        print(isodate + " " + note.getText())

        url =note.find("a")['href']
        #print(url)
        filename  = url.split("/")[-1]
        urllib.request.urlretrieve(url, f"./notas/{isodate}-{filename}.html")




if __name__ == '__main__':

    getLastPages()

    #filename = sys.argv[1]
    #getNotesFromPage(filename)

    date = sys.argv[1]
    getNotesFromDay(date)
