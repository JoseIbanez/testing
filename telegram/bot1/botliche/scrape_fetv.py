
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

class EventTV:
    date = None
    competition = None
    local = None
    away = None
    channels = []    

    def __repr__(self):
        return f"{self.date} {self.competition}: {self.local}-{self.away}"


FOLLOW_TEAMS = [ "Liverpool", "FC Barcelona", "Manchester City", "Real Madrid" ]
FOLLOW_COMPETITIONS = [ "Fórmula 1", "MotoGP" ]

class EventTVList:

    def __init__(self):
        self.list:list[EventTV] = []

    def scrape(self,filename:str):

        with open(filename,"r") as f:
            page = f.read()

        soup = BeautifulSoup(page, "html.parser")
        main_table = soup.find('table', {'class': 'tablaPrincipal'})

        row_counter = -1
        date = None

        for row in main_table.findChildren('tr'):

            cols = row.findChildren('td')
            row_counter += 1
            if row_counter == 0:

                m = re.search("(\d+/\d+/\d+)",cols[0].string)
                if m:
                    date = m.group(1)
                else:
                    date = ""
                continue
            
            if len(cols) == 4:
                e = parse_4_cols(cols,date)
            elif len(cols) == 5:
                e = parse_5_cols(cols,date)
            else:
                continue

            ignore = True

            if e.local in FOLLOW_TEAMS or e.away in FOLLOW_TEAMS:
                ignore = False

            if e.competition in FOLLOW_COMPETITIONS:
                ignore = False

            if ignore:
                continue



            self.list.append(e)

            print(e)

        return


def parse_4_cols(cols,date):

    e = EventTV()
    hour   =  cols[0].string.rstrip().lstrip()
    e.date = datetime.strptime(f"{date} {hour}", '%d/%m/%Y %H:%M')
    e.competition = cols[1].findChildren('span')[0].string.rstrip().lstrip()
    e.local  = None
    e.away  =  None
    e.channels = [ i.string for i in cols[3].findChildren('li')]   

    return e


def parse_5_cols(cols,date):

    e = EventTV()
    hour   =  cols[0].string.rstrip().lstrip()
    e.date = datetime.strptime(f"{date} {hour}", '%d/%m/%Y %H:%M')
    e.competition = cols[1].findChildren('label')[0].string.rstrip().lstrip()
    e.local  = cols[2].findChild('span').string
    e.away  =  cols[3].findChild('span').string
    e.channels = [ i.string for i in cols[4].findChildren('li')]   

    return e


def main():

    events = EventTVList()
    events.scrape("/home/ibanez/Projects/testing/telegram/bot1/sample-data/fetv.txt")

if __name__ == "__main__":
    main()


