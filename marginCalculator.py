# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 12:44:27 2022

@author: ulind
"""
# Importing important libraries
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns


def marginCalculator(stock,start_date = "2009-11-01" ,end_date = "2021-11-18"):
    '''This function returns the list of profits w.r.t margin percentage used'''
    margin = []
    profit = []
    for val in [0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5]:
        df = yf.download(stock, start=start_date, end=end_date)
        margin.append(val)
        df['sell'] =0
        df['buy'] =0
        # Predicting high and low price based on previous day's close price
        df['predhigh'] = df['Close'].shift(1)*(100+val)/100
        df['predlow'] = df['Close'].shift(1)*(100-val)/100
        # Creating a buy and sell counter to see if the predicted prices are met
        df.loc[df.predhigh <= df.High, ['sell']] = 1
        df.loc[df.predlow >= df.Low, ['buy']] = 1
        # Assigning final sell and buy prices  
        df.loc[(df.predhigh <= df.High), ['final_sell']] = df.predhigh # Price at which we are selling the shares
        df.loc[df.predlow >= df.Low, ['final_buy']] = df.predlow  # Price at which we are buying the shares
        # Squaring off the trades intraday iresspective of profits/loss
        df.loc[((df.sell==1)&(df.buy==0)),'final_buy'] = df.Close
        df.loc[((df.sell==0)&(df.buy==1)),'final_sell'] = df.Close
        # Creating new feature for profits through buying and selling shares everyday
        df['profit_buy'] = -100*(df.final_buy-df.Close)/df.final_buy  # Profit through buying shares at predicted low price
        df['profit_sell'] = 100*(df.final_sell-df.Close)/df.final_sell # Profit through selling shares at predicted high price  
        # Filling the null values
        df[['profit_sell','profit_buy']] = df[['profit_sell','profit_buy']].fillna(0)
        # Final profit
        df['profit'] = (df['profit_sell'])+(df['profit_buy'])
        profit.append(np.sum(df['profit']))
    return profit,margin,df