import requests
import time

def getNow(pair):
    return requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}}&tsyms={}'.format(*pair)).json()

def getPast(pair, daysBack, daysData):
    now = int(time.time())
    end = now-(24*60*60*daysBack)
    response = requests.get('https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&fromTs={}&limit={}&aggregate=1'.format(pair[0],pair[1],end,daysData))
    results = response.json()['Data']
    print(results)
    return results
