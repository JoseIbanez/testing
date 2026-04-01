import pandas as pd

url = "https://en.wikipedia.org/wiki/STOXX_Europe_600"


index_list = [
    {"name":"STOXX_Europe_600", "url":"https://en.wikipedia.org/wiki/STOXX_Europe_600", "table_index":2},
    {"name":"DAX", "url":"https://en.wikipedia.org/wiki/DAX", "table_index":4},
    {"name":"CAC_40", "url":"https://en.wikipedia.org/wiki/CAC_40", "table_index":4},
    {"name":"IBEX_35", "url":"https://en.wikipedia.org/wiki/IBEX_35", "table_index":2},
    {"name":"FTSE_MIB", "url":"https://en.wikipedia.org/wiki/FTSE_MIB", "table_index":1},
    {"name":"FTSE_100", "url":"https://en.wikipedia.org/wiki/FTSE_100", "table_index":6},
]


for index in index_list:
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    tables = pd.read_html(index["url"], storage_options={'User-Agent': 'Mozilla/5.0'})

    # The first table usually contains the components
    components_df = tables[index["table_index"]]
    print(index["name"])
    print(components_df.head())


    #Set index to Ticker
    components_df = components_df.set_index("Ticker")


    #Save to csv
    components_df.to_csv(f"./data/index/{index['name']}.csv")


    #print(components_df[['Ticker', 'Company']])
