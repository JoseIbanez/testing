
import requests
import time
import os
import re
from bs4 import BeautifulSoup, ResultSet, Tag
from datetime import datetime
import logging
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

class EventTV:
    date = None
    competition = None
    local = None
    away = None
    channels = []    

    def __repr__(self):

        if self.away:
            return f"{self.date} {self.competition}: {self.local}-{self.away}"
        else:
            return f"{self.date} {self.competition}: {self.local}"


FOLLOW_TEAMS = [ "Real Madrid", "FC Barcelona", 
                 "Manchester City", "Liverpool",
                 "C. Alcaraz" ]
FOLLOW_COMPETITIONS = [ "Fórmula 1", "MotoGP" ]
BANNED_CHANNELS = [ "DAZN (Regístrate)", 'MotoGP Videopass', 'ATP Tennis TV' ] 

FETV_URL = "https://www.futbolenlatv.es/deporte"
DATA_PATH =  os.environ.get("DATA_PATH", "/home/ibanez/Projects/testing/telegram/bot1/sample-data")
LOCAL_FILE = f"{DATA_PATH}/fetv.txt" 


class EventTVList:

    def __init__(self):
        self.list:list[EventTV] = []
        self.timeout = 4*3600
        self.lastupdate = 0

    def download(self,url:str,filename:str):

        try:
            age = int(time.time() - os.path.getmtime(filename))
        except OSError:
            age = self.timeout + 1
            pass

        if age < self.timeout:
            return

        time0 = time.time()
        response = requests.get(url)

        with open(filename,"w") as f:
            f.write(response.text)

        logger.info("Downloaded TV events, delay:%0.3f seg",(time.time()-time0))

    def scrape(self,filename:str):

        logger.info("Scraping page")
        time0 = time.time()
        with open(filename,"r") as f:
            page = f.read()

        soup = BeautifulSoup(page, "html.parser")
        table_list = soup.findAll('table', {'class': 'tablaPrincipal'})

        for table in table_list:
            self.scrape_table(table)

        logger.info("Page scraped, duration:%0.3f",time.time() -time0)



    def scrape_table(self,main_table):

        row_counter = -1
        date = None

        for row in main_table.findChildren('tr'): 

            cols = row.findChildren('td')

            row_counter += 1
            if row_counter == 0:
                date = parse_date(cols)
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

            e.channels = filter_channels(e.channels)
            self.list.append(e)
            logger.info(e)

        return

    def get_events(self):

        if not self.list or self.lastupdate + self.timeout < time.time():
            self.list = []
            self.download(FETV_URL, LOCAL_FILE)
            self.scrape(LOCAL_FILE)
            self.lastupdate = time.time()

        return


def parse_date(cols:ResultSet):
    """
    Parse date line
    """
    
    m = re.search("(\d+/\d+/\d+)",cols[0].string)
    date = m.group(1) if m else ""
    return date


def parse_datetime(date:str,hour:str):

    try:
        e_datetime = datetime.strptime(f"{date} {hour}", '%d/%m/%Y %H:%M')
    except ValueError:
        e_datetime = None
        pass

    if not e_datetime:
        try:
            e_datetime = datetime.strptime(f"{date}", '%d/%m/%Y')
        except ValueError:
            e_datetime = datetime.now()

    return e_datetime

def parse_competition(col:Tag):

    try:
        labels = col.findChildren('label')
        spans = col.findChildren('span')

        if labels and len(labels)>0:
            competition = labels[0].string
        elif spans and len(spans)>0:
            competition = spans[0].string
        else:
            logger.error("Col without competition, %s",col)
            competition = ""     

        competition = competition.rstrip().lstrip()
    except  (AttributeError, IndexError) as e:
        logger.error("Error:%s, for col:%s",e,col)
        competition = ""
    
    return competition


def parse_4_cols(cols:ResultSet,date):

    e = EventTV()
    hour   =  cols[0].string.rstrip().lstrip()
    e.date = parse_datetime(date,hour)
    e.competition = parse_competition(cols[1])
    e.local  = cols[2].text.rstrip().lstrip()
    e.away  =  None
    e.channels = [ i.string for i in cols[3].findChildren('li')]   
    return e


def parse_5_cols(cols:ResultSet,date):

    e = EventTV()
    hour   =  cols[0].string.rstrip().lstrip()
    e.date = parse_datetime(date,hour)
    e.competition = parse_competition(cols[1])
    e.local  = cols[2].findChild('span').string
    e.away  =  cols[3].findChild('span').string
    e.channels = [ i.string for i in cols[4].findChildren('li')]   
    return e


def filter_channels(channels_in):

    channels_out = []

    for name_in in channels_in:
        
        if name_in in BANNED_CHANNELS:
            continue
        
        m = re.search("([^\(]+) ?",name_in)
        if not m:
            continue
        
        name_out = m.group(1).rstrip()
        channels_out.append(name_out)

    return channels_out

def main():

    configure_loger()

    events = EventTVList()

    print (events.get_events())

if __name__ == "__main__":
    main()


