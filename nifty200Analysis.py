# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 12:48:31 2022

@author: ulind
"""
import numpy as np
import pandas as pd
import yfinance as yf
import shareAnalysis as sa

def nifty200Analysis(start_date,end_date,pct,close_off=15):
    '''Returns a dataframe with all the stocks in NIFTY 200 and 
       the profits they made based on the strategy'''
    nifty200_summary = pd.DataFrame(columns=['stock'])
    nifty200 = pd.read_csv('C://Users//ulind//Downloads//ind_nifty200list.csv')
    for j in range(len(nifty200)):
        print(nifty200['Company Name'][j])
        nifty200_summary.loc[j,'stock'] = nifty200['Company Name'][j]
        nifty200_summary.loc[j,'code'] = nifty200.code[j]
        profit,daily_data,success_rate,profit_sell,profit_buy = sa.shareAnalysis(stock=nifty200.code[j], start_date=start, end_date = end,pct=0.75)
        nifty200_summary.loc[j,'profit_sell'] = profit_sell
        nifty200_summary.loc[j,'profit_buy'] = profit_buy
        nifty200_summary.loc[j,'profit'] = profit
        nifty200_summary.loc[j,'successrate'] = success_rate
    return nifty200_summary