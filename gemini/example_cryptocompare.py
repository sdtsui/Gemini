import pandas as pd
import gemini
import cryptocompare as cc
import helpers
from datetime import *

pair = ['BTC','USD']    # Use ETH pricing data on the BTC market
startDate = datetime(2017,8,1)
endDate = datetime(2017,9,1)
# Request data from cryptocompare
data = cc.getPast(pair, startDate, endDate)

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data['date'] = pd.to_datetime(data['date'], unit='s')

def Logic(Account, Lookback):
    try:
        # Process dataframe to collect signals
        # Lookback = helpers.getSignals(Lookback)

        # Load into period class to simplify indexing
        Lookback = helpers.Period(Lookback)

        Today = Lookback.loc(0) # Current candle
        Yesterday = Lookback.loc(-1) # Previous candle
        print(Today)
        if Today['close'] < Yesterday['close']:
            ExitPrice = Today['close']
            for Position in Account.Positions:
                if Position.Type == 'Long':
                    Account.ClosePosition(Position, 0.5, ExitPrice)

        if Today['close'] > Yesterday['close']:
            Risk         = 0.03
            EntryPrice   = Today['close']
            EntryCapital = Account.BuyingPower*Risk
            if EntryCapital >= 0:
                Account.EnterPosition('Long', EntryCapital, EntryPrice)

    except ValueError:
        pass # Handles lookback errors in beginning of dataset

# Load the data into a backtesting class called Run
r = gemini.Run(data)

# Start backtesting custom logic with 1000 (BTC) intital capital
r.Start(1000, Logic)

r.Results()
r.Chart(ShowTrades=False)
