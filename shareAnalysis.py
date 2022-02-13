# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 12:45:50 2022

@author: ulind
"""
# Importing important libraries
import numpy as np
import pandas as pd
import yfinance as yf


#Finalized
def shareAnalysis(stock,start_date,end_date,pct,close_off=15):
    '''Returns the profit, successrate and details of the trade on stocks
       based on the given dates and cutoff time '''
    # Downloading the daily data
    daily_data = yf.download(stock, start=start_date, end=end_date)
    if len(daily_data)>0:
        # Downloading the hourly data
        hourly_data = yf.download(stock, start=start_date, end=end_date,interval="1h",auto_adjust=True)
        # Creating new columns in the dataframes
        hourly_data['hour'] = hourly_data.index.hour
        hourly_data['date'] = hourly_data.index.date
        daily_data['date'] = daily_data.index.date
        
        # Dropping the dates on which the share price is either capped or market is not fully functional (Eg.Muhurat trade etc.)
        for i in daily_data.date:
            if i not in hourly_data[hourly_data.hour==close_off].date.unique():  # Checking the data at 3.15PM (close_off time)
                print(i)
                daily_data.drop(i,inplace=True)      
                
        # Creating a column with the share price at 3.15 PM
        daily_data.loc[:,'close2'] = pd.Series(hourly_data[hourly_data['hour']==close_off].Close).values
        
        # Considering the day's low based on the hourly low price data
        daily_data.loc[:,'low_'] = hourly_data.groupby('date')['Low'].min()
        
        # Considering the day's high based on the hourly high price data
        daily_data.loc[:,'high_'] = hourly_data.groupby('date')['High'].max()
        
        # Predicting high and low price based on previous day's close price
        daily_data['predhigh'] = daily_data['Close'].shift(1)*(100+pct)/100
        daily_data['predlow'] = daily_data['Close'].shift(1)*(100-pct)/100
        
        # Creating a buy and sell counter to see if the predicted prices are met
        daily_data.loc[daily_data.predhigh <= daily_data.high_, ['sell']] = 1
        daily_data.loc[daily_data.predlow >= daily_data.low_, ['buy']] = 1
        
        # Assigning final sell and buy prices
        daily_data.loc[(daily_data.predhigh <= daily_data.high_), ['final_sell']] = daily_data.predhigh
        daily_data.loc[daily_data.predlow >= daily_data.low_, ['final_buy']] = daily_data.predlow
        
        #daily_data = daily_data[(daily_data.Open == daily_data.high_)|(daily_data.Open == daily_data.low_)]
        
        # Squaring off the trades at 3.15 PM
        daily_data.loc[((daily_data.sell==0)&(daily_data.buy==1)),'final_sell'] = daily_data.close2
        daily_data.loc[((daily_data.sell==1)&(daily_data.buy==0)),'final_buy'] = daily_data.close2
        
        daily_data['profit_buy'] = -100*(daily_data.final_buy-daily_data.close2)/daily_data.final_buy
        daily_data['profit_sell'] = 100*(daily_data.final_sell-daily_data.close2)/daily_data.final_sell
    
        # Calculating profits
        profit_sell = np.sum(daily_data.profit_sell)
        profit_buy = np.sum(daily_data.profit_buy)
        daily_data.fillna(0,inplace=True)
        daily_data['profit'] = (daily_data['profit_sell'])+(daily_data['profit_buy'])
        profit = profit_sell+profit_buy
    
        #  Calculating the successrate
        if len(daily_data)>0:
            success_rate = 100*len(daily_data[daily_data['profit']>0.20])/len(daily_data)  
            # A day's trade is considered a 'success' only when the day's profit is atleast 0.2% of the capital.
        else:
            success_rate = 'None'
        
        # Dropping the helper columns 
        daily_data.drop(['sell','Close','profit_sell','profit_buy','Adj Close','Volume','date','High','Low','buy'],axis=1,inplace=True)
    
        return profit,daily_data,success_rate,profit_sell,profit_buy
    return 0,0,0,0,0