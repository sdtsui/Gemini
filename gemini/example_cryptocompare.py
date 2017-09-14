import pandas as pd
import gemini
import cryptocompare as cc
import helpers
from datetime import *

pair = ['BTC','USD']    # Use ETH pricing data on the BTC market
daysBack = 0       # Grab data starting X days ago
daysData = 100       # From there collect X days of data
TradingInterval = 4 # Run trading logic every X days
# Request data from cryptocompare
data = cc.getPast(pair, daysBack, daysData)

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data['date'] = pd.to_datetime(data['time'], unit='s')

def Logic(Account, Lookback):
    try:
        # Load into period class to simplify indexing
        Lookback = helpers.Period(Lookback)

        Today = Lookback.loc(0) # Current candle
        Yesterday = Lookback.loc(-40) # Previous candle
        print('from {} to {}'.format(Yesterday['date'],Today))

        if Today['close'] < Yesterday['close']:
            ExitPrice = Today['close']
            for Position in Account.Positions:
                if Position.Type == 'Long':
                    Account.ClosePosition(Position, 1, ExitPrice)

        if Today['close'] > Yesterday['close']:
            EntryPrice   = Today['close']
            EntryCapital = Account.BuyingPower
            if EntryCapital > 0:
                Account.EnterPosition('Long', EntryCapital, EntryPrice)
    except ValueError:
        pass # Handles lookback errors in beginning of dataset

# Load the data into a backtesting class called Run
r = gemini.Run(data)

# Start backtesting custom logic with 1000 (BTC) intital capital and 2 day trading interval
r.Start(1000, Logic, TradingInterval)

r.Results()
r.Chart(ShowTrades=False)
