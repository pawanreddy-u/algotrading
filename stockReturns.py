# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 12:29:04 2022

@author: ulind
"""
# Importing important libraries
import numpy as np
import pandas as pd
import yfinance as yf


def stockReturns(stock,start_date = "2009-11-01" ,end_date = "2021-11-18"):
    '''Returns a dataframe with all the information about the trades'''
    # Downloading the data
    df = yf.download(stock, start=start_date, end=end_date)  
    val = 0.75 # The margin we are expecting from a potential succesful trade
    # Predicting high and low price based on previous day's close price
    df['predhigh'] = df['Close'].shift(1)*(100+val)/100
    df['predlow'] = df['Close'].shift(1)*(100-val)/100
    # Creating a buy and sell counter to see if the predicted prices are met
    df.loc[df.predhigh <= df.High, ['sell']] = 1
    df.loc[df.predlow >= df.Low, ['buy']] = 1
    # Assigning final sell and buy prices
    df.loc[(df.predhigh <= df.High), ['final_sell']] = df.predhigh  # Price at which we are selling the shares
    df.loc[df.predlow >= df.Low, ['final_buy']] = df.predlow  # Price at which we are buying the shares
    # Squaring off the trades intraday iresspective of profits/loss
    df.loc[((df.sell==1)&(df.buy==0)),'final_buy'] = df.Close
    df.loc[((df.sell==0)&(df.buy==1)),'final_sell'] = df.Close  
    # Creating new feature for profits through buying and selling shares everyday
    df['profit_buy'] = -100*(df.final_buy-df.Close)/df.final_buy  # Profit through buying shares at predicted low price
    df['profit_sell'] = 100*(df.final_sell-df.Close)/df.final_sell   # Profit through selling shares at predicted high price
    # Filling the null values
    df[['profit_sell','profit_buy']] = df[['profit_sell','profit_buy']].fillna(0)
    # Final profit
    df['profit'] = (df['profit_sell'])+(df['profit_buy'])
    # Dropping columns of less importance
    df.drop(['sell','Close','Adj Close','Volume','High','Low','buy'],axis=1,inplace=True)
    return df