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

st.title("SWING ANALYSIS")


tickers = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
stocks = tickers.Symbol.to_list()


ticker_symbol = st.selectbox("Choose your sector",stocks)
start_date=st.date_input("START DATE")
end_date=st.date_input("END DATE")




plt.rcParams['figure.figsize'] = [26, 15]
plt.rc('font', size=30)

ticker = yfinance.Ticker(ticker_symbol+'.NS')
df = ticker.history(interval='1d', start=start_date, end=end_date)

df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)

df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

  

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
def plot_levels():
  fig, ax = plt.subplots()
  candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
  date_format = mpl_dates.DateFormatter('%d %b %Y')
  ax.xaxis.set_major_formatter(date_format)
  fig.autofmt_xdate()
  fig.tight_layout()

  for level, level_type in zip(levels, level_types):
    plt.hlines(level[1],
              xmin = df['Date'][level[0]],
              xmax = max(df['Date']),
              colors = 'blue')
    plt.text(df['Date'][level[0]], level[1], (str(level_type) + ': ' + str(level[1]) + ' '), ha='right', va='center', fontweight='bold', fontsize='x-small')
    plt.title('Support and Resistance levels for ' + ticker_symbol, fontsize=24, fontweight='bold')
    

  # Clean noise in data by discarding a level if it is near another
  # (i.e. if distance to the next level is less than the average candle size for any given day - this will give a rough estimate on volatility)
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
previous_averaged_volume = hist['Volume'].iloc[1:4:1].mean()
todays_volume = hist['Volume'][-1]
previous_close = hist['Close'][-2]
current_close = hist['Close'][-1]


st.pyplot(plot_levels())
st.set_option('deprecation.showPyplotGlobalUse', False)



################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
st.title("SENTIMENT ANALYSIS")

keyword=st.text_input("KEYWORD")
limit=st.number_input("LIMIT", min_value=1000, max_value=5000, value=1000, step=1000)

pos=0
neg=0
neu=0
consumer_key="c75e056gZU0V72rHCuB40KfB5"
consumer_sec='dRlMoJKTN7HTnP5amYZeKT2zKhB5WLhF34lowiGesXKmuV7G37'
access_token="1390979922798157824-7Z64W6WpUhwTt7WSoBX3rrdjq5njkI"
access_token_sec="1A3CMZbd3G0WBldgRORBcD8CLaPjsKQ2vr1AyqOyaYLK9"


def stop_word_removal(s):
    stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    a=''
    for i in s.split(' '):
        if i not in stop_words:
            a=a+i+' '
    return a

def stemmer(s):
    ps=PorterStemmer()
    a=''
    for i in s.split(' '):
        a=a+ps.stem(i)+' ' 
    return a




# connected to jump server of twitter
auth=tweepy.OAuthHandler(consumer_key,consumer_sec)

# now we can connect from jump server to web server of twitter
auth.set_access_token(access_token,access_token_sec)

# now we can connect to API storge server of twitter
api=tweepy.API(auth)


tweets = tweepy.Cursor(api.search_tweets, q=keyword, count=100000, tweet_mode='extended').items(limit)



try:
    columns = ['User', 'Tweet']
    data = []

    for tweet in tweets:
        word=tweet.full_text
        word=stop_word_removal(word)
        word=stemmer(word)
        word=re.sub(r'(\s)#\w+|(\s)@\w+|rt|http\S+|[^\w]',' ',word)
        word=re.sub(' {2,}',' ',word)
        word=word.lower()
        analysis=TextBlob(word) # here it will apply NLP\
        
        if analysis.sentiment.polarity > 0:
            #print("posative")
            pos=pos+1
        elif analysis.sentiment.polarity == 0 :
            #print("Neutral")
            neu=neu+1
        else :
            #print("Negative")
            neg=neg+1
        
    # ploting graphs
    plt.xlabel("tags")
    plt.ylabel("polarity")
    #plt.bar(['pos','neg','neu'],[pos,neg,neu])
    
    #st.pyplot(plt.pie([pos,neg,neu],labels=['pos','neg','neu'],autopct="%1.1f%%"))
    labels=['pos','neg','neu']
    sizes = [pos,neg,neu]
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)
except:
    st.subheader("Plese enter keyword inside KEYWORD block")


