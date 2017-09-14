import requests
import time
from datetime import *

def daterange(startDate, endDate):
    for n in range(int ((endDate - startDate).days)):
        yield startDate + timedelta(n)

def getNow(pair):
    return requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}}&tsyms={}'.format(*pair)).json()

def getPast(pair, startDate, endDate):
    results = []
    for day in daterange(startDate, endDate):
        # print(day.strftime("%Y-%m-%d"))
        day_ts = int(day.timestamp())
        # print(day_ts)
        response = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}&ts={}'.format(pair[0],pair[1],day_ts)).json()
        # print(response)
        close_price = response[pair[0]][pair[1]]
        response_formatted = {'date':day_ts, 'close':close_price, 'open':close_price}
        # print(response_formatted)
        results.append(response_formatted)
        print('.')
    return results

# pair = ['BTC','USD']    # Use ETH pricing data on the BTC market
# startDate = datetime(2017,8,1)
# endDate = datetime(2017,9,1)
# # Request data from cryptocompare
# data = getPast(pair, startDate, endDate)
