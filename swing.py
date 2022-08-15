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



ans=set()

interval=['5m','15m','1h','1d','1wk','1mo']



sectors={
    'NIFTY_AUTO':['BHARATFORG','EICHERMOT','ESCORTS','SONACOMS','ASHOKLEY','MRF','BALKRISIND','BAJAJ-AUTO','TATAMOTORS','M&M','TIINDIA','TVSMOTOR','BOSCHLTD','HEROMOTOCO','MARUTI'],
    'NIFTY_METAL':['SAIL','TATASTEEL','APLAPOLLO','VEDL','JSL','JINDALSTEL','WELCORP','ADANIENT','NATIONALUM','HINDCOPPER','HINDALCO','JSWSTEEL','HINDZINC','MOIL','RATNAMANI'],
    'NIFTY_IT':['LTTS','WIPRO','TCS','HCLTECH','TECHM','INFY','LTI','COFORGE','MPHASIS','MINDTREE'],
    'NIFTY_BANK':['ICICIBANK','SBIN','AXISBANK','HDFCBANK','INDUSINDBK','BANKBARODA','FEDERALBNK','IDFCFIRSTB','PNB','KOTAKBANK','BANDHANBNK','AUBANK'],
    'NIFTY_ENERGY':['ONGC','NTPC','GAIL','POWERGRID','BPCL','RELIANCE','TATAPOWER','ADANITRANS','IOC','ADANIGREEN']


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
  previous_averaged_volume = hist['Volume'].iloc[1:4:1].mean()
  todays_volume = hist['Volume'][-1]
  previous_close = hist['Close'][-2]
  current_close = hist['Close'][-1]
  for i in support_resistance.keys():
    if ticker.info['regularMarketPrice']>=i*0.97 and ticker.info['regularMarketPrice']<=i*1.03 and todays_volume > previous_averaged_volume:
      ans.add(ticker_symbol)
      
if len(ans)!=0:
    for i in ans:
        st.info(i[:-3])
else:
    st.warning("NO STOCKS ARE AT SUPOORT OR RESISTANCE LEVEL IN "+sector)

  







'''





'''

components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;width:100%" /> """)


################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################


st.title("SWING ANALYSIS 2")



stocks=['3MINDIA'
,'ABB'
,'ACC'
,'AIAENG'
,'APLAPOLLO'
,'AUBANK'
,'AARTIDRUGS'
,'AAVAS'
,'ABBOTINDIA'
,'ADANIENT'
,'ADANIGREEN'
,'ADANIPORTS'
,'ATGL'
,'ADANITRANS'
,'ABCAPITAL'
,'ABFRL'
,'ABSLAMC'
,'ADVENZYMES'
,'AEGISCHEM'
,'AFFLE'
,'AJANTPHARM'
,'APLLTD'
,'ALKEM'
,'ALKYLAMINE'
,'ALLCARGO'
,'ALOKINDS'
,'AMARAJABAT'
,'AMBER'
,'AMBUJACEM'
,'ANGELONE'
,'ANURAS'
,'APOLLOHOSP'
,'APOLLOTYRE'
,'APTUS'
,'ASAHIINDIA'
,'ASHOKLEY'
,'ASIANPAINT'
,'ASTERDM'
,'ASTRAZEN'
,'ASTRAL'
,'ATUL'
,'AUROPHARMA'
,'AVANTIFEED'
,'DMART'
,'AXISBANK'
,'BASF'
,'BSE'
,'BAJAJ-AUTO'
,'BAJAJELEC'
,'BAJFINANCE'
,'BAJAJFINSV'
,'BAJAJHLDNG'
,'BALAMINES'
,'BALKRISIND'
,'BALRAMCHIN'
,'BANDHANBNK'
,'BANKBARODA'
,'BANKINDIA'
,'MAHABANK'
,'BATAINDIA'
,'BAYERCROP'
,'BERGEPAINT'
,'BDL'
,'BEL'
,'BHARATFORG'
,'BHEL'
,'BPCL'
,'BHARTIARTL'
,'BIOCON'
,'BIRLACORPN'
,'BSOFT'
,'BLUEDART'
,'BLUESTARCO'
,'BBTC'
,'BORORENEW'
,'BOSCHLTD'
,'BRIGADE'
,'BCG'
,'BRITANNIA'
,'MAPMYINDIA'
,'CCL'
,'CESC'
,'CGPOWER'
,'CRISIL'
,'CSBBANK'
,'CAMPUS'
,'CANFINHOME'
,'CANBK'
,'CAPLIPOINT'
,'CGCL'
,'CARBORUNIV'
,'CASTROLIND'
,'CEATLTD'
,'CENTRALBK'
,'CDSL'
,'CENTURYPLY'
,'CENTURYTEX'
,'CERA'
,'CHALET'
,'CHAMBLFERT'
,'CHEMPLASTS'
,'CHOLAHLDNG'
,'CHOLAFIN'
,'CIPLA'
,'CUB'
,'CLEAN'
,'COALINDIA'
,'COCHINSHIP'
,'COFORGE'
,'COLPAL'
,'CAMS'
,'CONCOR'
,'COROMANDEL'
,'CREDITACC'
,'CROMPTON'
,'CUMMINSIND'
,'CYIENT'
,'DCMSHRIRAM'
,'DLF'
,'DABUR'
,'DALBHARAT'
,'DEEPAKNTR'
,'DELHIVERY'
,'DELTACORP'
,'DEVYANI'
,'DHANI'
,'DBL'
,'DIVISLAB'
,'DIXON'
,'LALPATHLAB'
,'DRREDDY'
,'EIDPARRY'
,'EIHOTEL'
,'EPL'
,'EASEMYTRIP'
,'EDELWEISS'
,'EICHERMOT'
,'ELGIEQUIP'
,'EMAMILTD'
,'ENDURANCE'
,'ENGINERSIN'
,'EQUITAS'
,'EQUITASBNK'
,'ERIS'
,'ESCORTS'
,'EXIDEIND'
,'FDC'
,'NYKAA'
,'FEDERALBNK'
,'FACT'
,'FINEORG'
,'FINCABLES'
,'FINPIPE'
,'FSL'
,'FORTIS'
,'GRINFRA'
,'GAIL'
,'GMMPFAUDLR'
,'GMRINFRA'
,'GALAXYSURF'
,'GARFIBRES'
,'GICRE'
,'GLAND'
,'GLAXO'
,'GLS'
,'GLENMARK'
,'GOCOLORS'
,'GODFRYPHLP'
,'GODREJAGRO'
,'GODREJCP'
,'GODREJIND'
,'GODREJPROP'
,'GRANULES'
,'GRAPHITE'
,'GRASIM'
,'GESHIP'
,'GRINDWELL'
,'GUJALKALI'
,'GAEL'
,'FLUOROCHEM'
,'GUJGASLTD'
,'GNFC'
,'GPPL'
,'GSFC'
,'GSPL'
,'HEG'
,'HCLTECH'
,'HDFCAMC'
,'HDFCBANK'
,'HDFCLIFE'
,'HFCL'
,'HLEGLAS'
,'HAPPSTMNDS'
,'HATHWAY'
,'HATSUN'
,'HAVELLS'
,'HEMIPROP'
,'HEROMOTOCO'
,'HIKAL'
,'HINDALCO'
,'HGS'
,'HAL'
,'HINDCOPPER'
,'HINDPETRO'
,'HINDUNILVR'
,'HINDZINC'
,'POWERINDIA'
,'HOMEFIRST'
,'HONAUT'
,'HUDCO'
,'HDFC'
,'ICICIBANK'
,'ICICIGI'
,'ICICIPRULI'
,'ISEC'
,'IDBI'
,'IDFCFIRSTB'
,'IDFC'
,'IFBIND'
,'IIFL'
,'IIFLWAM'
,'IRB'
,'IRCON'
,'ITC'
,'ITI'
,'INDIACEM'
,'IBULHSGFIN'
,'IBREALEST'
,'INDIAMART'
,'INDIANB'
,'IEX'
,'INDHOTEL'
,'IOC'
,'IOB'
,'IRCTC'
,'IRFC'
,'INDIGOPNTS'
,'ICIL'
,'INDOCO'
,'IGL'
,'INDUSTOWER'
,'INDUSINDBK'
,'INFIBEAM'
,'NAUKRI'
,'INFY'
,'INOXLEISUR'
,'INTELLECT'
,'INDIGO'
,'IPCALAB'
,'JBCHEPHARM'
,'JKCEMENT'
,'JKLAKSHMI'
,'JKPAPER'
,'JMFINANCIL'
,'JSWENERGY'
,'JSWSTEEL'
,'JAMNAAUTO'
,'JSL'
,'JINDALSTEL'
,'JUBLFOOD'
,'JUBLINGREA'
,'JUBLPHARMA'
,'JUSTDIAL'
,'JYOTHYLAB'
,'KPRMILL'
,'KEI'
,'KNRCON'
,'KPITTECH'
,'KRBL'
,'KAJARIACER'
,'KALPATPOWR'
,'KALYANKJIL'
,'KANSAINER'
,'KARURVYSYA'
,'KEC'
,'KOTAKBANK'
,'KIMS'
,'L&TFH'
,'LTTS'
,'LICHSGFIN'
,'LAXMIMACH'
,'LTI'
,'LT'
,'LATENTVIEW'
,'LAURUSLABS'
,'LXCHEM'
,'LICI'
,'LINDEINDIA'
,'LUPIN'
,'LUXIND'
,'MMTC'
,'MOIL'
,'MRF'
,'MTARTECH'
,'LODHA'
,'MGL'
,'M&MFIN'
,'M&M'
,'MAHINDCIE'
,'MHRIL'
,'MAHLOG'
,'MANAPPURAM'
,'MRPL'
,'MARICO'
,'MARUTI'
,'MASTEK'
,'MFSL'
,'MAXHEALTH'
,'MAZDOCK'
,'MEDPLUS'
,'METROBRAND'
,'METROPOLIS'
,'MINDTREE'
,'MOTILALOFS'
,'MPHASIS'
,'MCX'
,'MUTHOOTFIN'
,'NATCOPHARM'
,'NBCC'
,'NCC'
,'NESCO'
,'NHPC'
,'NLCINDIA'
,'NOCIL'
,'NTPC'
,'NH'
,'NATIONALUM'
,'NAVINFLUOR'
,'NAZARA'
,'NESTLEIND'
,'NETWORK18'
,'NAM-INDIA'
,'NUVOCO'
,'OBEROIRLTY'
,'ONGC'
,'OIL'
,'PAYTM'
,'OFSS'
,'ORIENTELEC'
,'POLICYBZR'
,'PCBL'
,'PIIND'
,'PNBHOUSING'
,'PNCINFRA'
,'PVR'
,'PAGEIND'
,'PERSISTENT'
,'PETRONET'
,'PFIZER'
,'PHOENIXLTD'
,'PIDILITIND'
,'POLYMED'
,'POLYCAB'
,'POLYPLEX'
,'POONAWALLA'
,'PFC'
,'POWERGRID'
,'PRAJIND'
,'PRESTIGE'
,'PRINCEPIPE'
,'PRSMJOHNSN'
,'PRIVISCL'
,'PGHL'
,'PGHH'
,'PNB'
,'QUESS'
,'RBLBANK'
,'RECLTD'
,'RHIM'
,'RITES'
,'RADICO'
,'RVNL'
,'RAILTEL'
,'RAIN'
,'RAJESHEXPO'
,'RALLIS'
,'RCF'
,'RATNAMANI'
,'RTNINDIA'
,'REDINGTON'
,'RELAXO'
,'RELIANCE'
,'RBA'
,'ROSSARI'
,'ROUTE'
,'SBICARD'
,'SBILIFE'
,'SIS'
,'SJVN'
,'SKFINDIA'
,'SRF'
,'SANOFI'
,'SAPPHIRE'
,'SAREGAMA'
,'SCHAEFFLER'
,'SEQUENT'
,'SFL'
,'SHILPAMED'
,'SCI'
,'SHREECEM'
,'RENUKA'
,'SRTRANSFIN'
,'SHYAMMETL'
,'SIEMENS'
,'SOBHA'
,'SOLARINDS'
,'SOLARA'
,'SONACOMS'
,'SONATSOFTW'
,'SPICEJET'
,'STARHEALTH'
,'SBIN'
,'SAIL'
,'SWSOLAR'
,'STLTECH'
,'STAR'
,'SUDARSCHEM'
,'SUMICHEM'
,'SPARC'
,'SUNPHARMA'
,'SUNTV'
,'SUNDARMFIN'
,'SUNDRMFAST'
,'SUNTECK'
,'SUPRAJIT'
,'SUPREMEIND'
,'SUVENPHAR'
,'SUZLON'
,'SYMPHONY'
,'SYNGENE'
,'TCIEXP'
,'TCNSBRANDS'
,'TTKPRESTIG'
,'TV18BRDCST'
,'TVSMOTOR'
,'TANLA'
,'TATACHEM'
,'TATACOFFEE'
,'TATACOMM'
,'TCS'
,'TATACONSUM'
,'TATAELXSI'
,'TATAINVEST'
,'TATAMTRDVR'
,'TATAMOTORS'
,'TATAPOWER'
,'TATASTLLP'
,'TATASTEEL'
,'TTML'
,'TEAMLEASE'
,'TECHM'
,'NIACL'
,'RAMCOCEM'
,'THERMAX'
,'THYROCARE'
,'TIMKEN'
,'TITAN'
,'TORNTPHARM'
,'TORNTPOWER'
,'TRENT'
,'TRIDENT'
,'TRIVENI'
,'TRITURBINE'
,'TIINDIA'
,'UCOBANK'
,'UFLEX'
,'UNOMINDA'
,'UPL'
,'UTIAMC'
,'ULTRACEMCO'
,'UNIONBANK'
,'UBL'
,'MCDOWELL-N'
,'VGUARD'
,'VMART'
,'VIPIND'
,'VAIBHAVGBL'
,'VAKRANGEE'
,'VTL'
,'VARROC'
,'VBL'
,'VEDL'
,'VENKEYS'
,'VIJAYA'
,'VINATIORGA'
,'IDEA'
,'VOLTAS'
,'WELCORP'
,'WELSPUNIND'
,'WESTLIFE'
,'WHIRLPOOL'
,'WIPRO'
,'WOCKPHARMA'
,'YESBANK'
,'ZFCVINDIA'
,'ZEEL'
,'ZENSARTECH'
,'ZOMATO'
,'ZYDUSLIFE'
,'ZYDUSWELL'
,'ECLERX']


selected_interval=st.selectbox("SELECT_INTERVAL",interval,index=3)

ticker_symbol = st.selectbox("Choose your sector",stocks)


if selected_interval in ('5m','15m','1h'):
    d = datetime.today() - timedelta(days=59)
    
    start_date2=st.date_input("START DATE",value=d,disabled=True)
else:
    start_date2=st.date_input("START DATE")
end_date2=st.date_input("END DATE")





plt.rcParams['figure.figsize'] = [26, 15]
plt.rc('font', size=30)

ticker = yfinance.Ticker(ticker_symbol+'.NS')
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
df = ticker.history(interval='1d', start=start_date2, end=end_date2)

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


'''





'''

components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;width:100%" /> """)


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


