import requests
import time
from datetime import *

def daterange(startDate, endDate):
    for n in range(int ((endDate - startDate).days)):
        yield startDate + timedelta(n)

def getNow(pair):
    return requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}}&tsyms={}'.format(*pair)).json()

def getPast(pair, startDate, endDate):
    for day in daterange(startDate, endDate):
        print(day.strftime("%Y-%m-%d"))
        print(int(day.timestamp()))
        response = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}&ts={}'.format(pair[0],pair[1],int(day.timestamp())))
        print(response.json())
        # return response.json()
