import streamlit as st
import pandas as pd
import numpy as np
import yfinance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import re
import tweepy
import matplotlib.pyplot as plt
from  textblob import TextBlob 
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
import streamlit.components.v1 as components
from datetime import datetime, timedelta



ans=[]

interval=['5m','15m','1h','1d','1wk','1mo']



sectors={
    'NIFTY_AUTO':['BHARATFORG','EICHERMOT','ESCORTS','SONACOMS','ASHOKLEY','MRF','BALKRISIND','BAJAJ-AUTO','TATAMOTORS','M&M','TIINDIA','TVSMOTOR','BOSCHLTD','HEROMOTOCO','MARUTI','AMARAJABAT','APOLLOTYRE','ENDURANCE','EXIDEIND','JKTYRE','SUNDRMFAST','SUPRAJIT','VARROC'],
    'NIFTY_METAL':['SAIL','TATASTEEL','APLAPOLLO','VEDL','JSL','JINDALSTEL','WELCORP','ADANIENT','NATIONALUM','HINDCOPPER','HINDALCO','JSWSTEEL','HINDZINC','MOIL','RATNAMANI','COALINDIA','NMDC'],
    'NIFTY_IT':['LTTS','WIPRO','TCS','HCLTECH','TECHM','INFY','LTI','COFORGE','MPHASIS','MINDTREE','AFFLE','TATAELXSI','PERSISTENT','HAPPSTMNDS'],
    'NIFTY_BANK':['ICICIBANK','SBIN','AXISBANK','HDFCBANK','INDUSINDBK','BANKBARODA','FEDERALBNK','IDFCFIRSTB','PNB','KOTAKBANK','BANDHANBNK','AUBANK'],
    'NIFTY_ENERGY':['ONGC','NTPC','GAIL','POWERGRID','BPCL','RELIANCE','TATAPOWER','ADANITRANS','IOC','ADANIGREEN','ADANITRANS','POWERGRID'],
    'NIFTY_FMGC':['BRITANNIA','COLPAL','DABUR','EMAMILTD','GODREJCP','HINDUNILVR','ITC','MARICO','NESTLEIND','PGHH','RADICO','TATACONSUM','UBL','MCDOWELL-N','VBL'],
    'DIGITAL_INDIA':['BHARTIARTL','TATACOMM','CAMS','IEX','AFFLE','INDIAMART','IRCTC','NAUKRI','STLTECH','CDSL'],
    'AGRICULTURE':['BAYERCROP','BHARATRAS','CHAMBLFERT','DHANUKA','FACT','GSFC','NFL','PIIND','RCF','SHARDACROP','UPL','ESCORTS','GODREJAGRO','VSTTILLERS','M&M','AVANTIFEED','KSCL','DCMSHRIRAM','RENUKA','EIDPARRY'],
    'NIFTY_INFRA':['ACC','ADANIPORTS','AMBUJACEM','APOLLOHOSP','ASHOKLEY','BALKRISIND','BPCL','BHARTIARTL','CONCOR','DLF','GAIL','GODREJPROP','GRASIM','HINDPETRO','IOC','IGL','INDUSTOWER','INDIGOPNTS','LT','MRF','NTPC','ONGC','PETRONET','POWERGRID','RELIANCE','SHREECEM','SIEMENS','TATAPOWER','ULTRACEMCO'],
    'NIFTY_EV':['AMARAJABAT','MOTHERSON','SUNDRMFAST','ENDURANCE','SONACOMS','GREAVESCOT','HEROMOTOCO','IOC','KPITTECH','M&M','POWERGRID','TATAPOWER','TATAELXSI','OLECTRA','TATAMOTORS']
	
}





st.title("SWING ANALYSIS")

selected_interval=st.selectbox("INTERVAL",interval,index=3)
sector=st.selectbox("SECTORS",sectors.keys())


if selected_interval in ('5m','15m','1h'):
    d = datetime.today() - timedelta(days=59)
    
    start_date2=st.date_input("START_DATE",value=d,disabled=True)
else:
    
    start_date2=st.date_input("START_DATE")
end_date2=st.date_input("END_DATE")

for ticker_symbol in sectors[sector]:
  ticker = yfinance.Ticker(ticker_symbol+'.NS')
  # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
  df = ticker.history(interval=selected_interval, start=start_date2, end=end_date2)

  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)

  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

  ######################################################################

  # Create two functions to calculate if a level is SUPPORT or a RESISTANCE level through fractal identification
  def is_Suppport_Level(df, i):
    support = df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] and df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]
    return support


  def is_Resistance_Level(df, i):
    resistance = df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] and df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]
    return resistance

  # Creating a list and feeding it the identified support and resistance levels via the Support and Resistance functions
  levels = []
  level_types = []
  for i in range(2, df.shape[0] - 2):

    if is_Suppport_Level(df, i):
      levels.append((i, df['Low'][i].round(2)))
      level_types.append('Support')

    elif is_Resistance_Level(df, i):
      levels.append((i, df['High'][i].round(2)))
      level_types.append('Resistance')

  # Plotting the data
  
  mean = np.mean(df['High'] - df['Low'])

  # This function, given a price value, returns True or False depending on if it is too near to some previously discovered key level.
  def distance_from_mean(level):
    return np.sum([abs(level - y) < mean for y in levels]) == 0


  ######################################################################################

  # Optimizing the analysis by adjusting the data and eliminating the noise from volatility that is causing multiple levels to show/overlapp
  levels = []
  level_types = []
  for i in range(2, df.shape[0] - 2):

    if is_Suppport_Level(df, i):
      level = df['Low'][i].round(2)

      if distance_from_mean(level):
        levels.append((i, level))
        level_types.append('Support')

    elif is_Resistance_Level(df, i):
      level = df['High'][i].round(2)

      if distance_from_mean(level):
        levels.append((i, level))
        level_types.append('Resistance')


  support_resistance={}
  for i in range(len(levels)):
      support_resistance[levels[i][1]]=level_types[i]


  hist = ticker.history(period="5d")
  #previous_averaged_volume = hist['Volume'].iloc[1:4:1].mean()
  #todays_volume = hist['Volume'][-1]
  previous_close = hist['Close'][-2]
  current_close = hist['Close'][-1]
  for i in support_resistance.keys():
    if ticker.info['regularMarketPrice']>=i*0.97 and ticker.info['regularMarketPrice']<=i*1.03 :
      ans.append(ticker_symbol)

    
if len(ans)!=0:
    for i in set(ans):
        st.info(i)
else:
    st.warning("NO STOCKS ARE AT SUPOORT OR RESISTANCE LEVEL IN "+sector)

  







'''





'''

components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;width:100%" /> """)


################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################

