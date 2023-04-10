

class Symbol:
    id = None       
    displayName = None
    marketState = None
    previousClose = None
    lastPrice = None
    currency = None
    priceVariation = None
    lastCheck = None

    def __repr__(self):

        marketState = "" if self.marketState == "OPEN" else self.marketState
        currency = f"{self.currency}" if self.currency else ""
        lastprice = f"{self.lastPrice:.3f} {currency}" if self.lastPrice else "-"
        var = f"{self.priceVariation:+.2f}%" if self.priceVariation else "" 

        result = f"{self.id} {self.displayName}:\n  LastPrice:{lastprice} {var} {marketState}" 

        return result