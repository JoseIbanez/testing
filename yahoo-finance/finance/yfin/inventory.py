
import pandas as pd
import yfinance as yf
import logging
import sqlite3

DB_PATH = "data/inventory.db"


INDEX_SUFIX_PER_COUNTRY = {
    "Denmark": ".CO",
    "Finland": ".HE",
    "France": ".PA",
    "Germany": ".DE",
    "Italy": ".MI",
    "Netherlands": ".AS",
    "Spain": ".MC",
    "Sweden": ".ST",
    "Switzerland": ".SW",
    "United Kingdom": ".L",
    }

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_index(index_name:str):
    """
    Parse the index csv file
    Update ticket name to yahoo finance ticket name if necessary
    Query yahoo finance for sector and industry information
    Insert update information into the sqlite database
    """

    #Read the csv index file in pandas
    path = f"data/index/{index_name}.csv"
    df = pd.read_csv(path)
    df.set_index("Ticker", inplace=True)

    conn = sqlite3.connect(DB_PATH)


    # Update ticket name to yahoo finance ticket name if necessary
    counter = 0
    for row in df.itertuples():
        ticker = row.Index
        print(ticker)

        # Test only first 10 rows
        counter += 1
        if counter > 50:
            break
            #pass

        if "." not in ticker:

            if  "STOXX" in index_name:
                country = row.Country
                if country in INDEX_SUFIX_PER_COUNTRY:
                    ticker += INDEX_SUFIX_PER_COUNTRY[country]
                    logger.info(f"Updated ticket: {ticker}")
                else:
                    logger.warning(f"Country {country} not found in INDEX_SUFIX_PER_COUNTRY, skipping ticket {ticker}")

            elif index_name == "FTSE_100":
                ticker += ".L"
                logger.info(f"Updated ticket: {ticker}")


        # Query yahoo finance for sector and industry information
        stock = yf.Ticker(ticker)
        info = stock.info
        # logger.info("Queried yahoo finance for ticker: %s", info)
        sector = info.get("sectorKey", "N/A")
        industry = info.get("industryKey", "N/A")
        shortName = info.get("shortName", "N/A")
        logger.info("Ticker: %s, Sector: %s, Name: %s, Industry: %s", ticker, sector, shortName, industry)


        #Insert update information into the sqlite database
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO stocks
                    (ticker, name, sector, industry) VALUES (?, ?, ?, ?)''', 
                    (ticker, shortName, sector, industry))

        conn.commit()


    conn.close()



def create_db():
    """
    Create the sqlite database if it doesn't exist
    """


    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
              ticker text primary key, 
              name text, 
              sector text, 
              industry text
              )''')
    conn.commit()
    conn.close()



def main():

    create_db()

    parse_index("STOXX_Europe_600")
    parse_index("IBEX_35")


if __name__ == "__main__":    
    main()