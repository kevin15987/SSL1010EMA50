import gemini
import ccxt
import pandas as pd
import time
import datetime
from datetime import timedelta


import pandas_ta as ta

#Gemini Info
r = gemini.PrivateClient("ACCOUNT KEY", "PRIVATE KEY")

gemini = ccxt.gemini()
ticker = "ETH/USD"
ticker_g = "ETHUSD"
# ssl_ohlcv = gemini.fetch_ohlcv(ticker,timeframe='1h')
# dfSSL = pd.DataFrame(ssl_ohlcv, columns=['date','open','high','low','close','volume'])
# dfSSL['date'] = pd.to_datetime(dfSSL['date'], unit='ms')
# dfSSL['date'] = dfSSL['date'] + datetime.timedelta(hours=-4)
# dfSSL.set_index('date',inplace=True)

# smaHigh = ta.sma(dfSSL['high'],length=10)
# smaLow = ta.sma(dfSSL['low'],length=10)


ema_ohlcv = gemini.fetch_ohlcv(ticker,timeframe='5m')
dfEMA = pd.DataFrame(ema_ohlcv, columns =['date','open','high','low','close','volume'])
dfEMA['date'] = pd.to_datetime(dfEMA['date'], unit='ms')
dfEMA['date'] = dfEMA['date'] + datetime.timedelta(hours=-4)
dfEMA.set_index('date',inplace=True)

emaClose = ta.ema(dfEMA['close'],length=50)


previous_candle = dfEMA.iloc[-2]
current_candle = dfEMA.iloc[-1]


#Testing Whether SSL is treding Up or Down every 5 minutes
while True:
    try:
        ssl_ohlcv = gemini.fetch_ohlcv(ticker,timeframe='1h')
        dfSSL = pd.DataFrame(ssl_ohlcv, columns=['date','open','high','low','close','volume'])
        dfSSL['date'] = pd.to_datetime(dfSSL['date'], unit='ms')
        dfSSL['date'] = dfSSL['date'] + datetime.timedelta(hours=-4)
        dfSSL.set_index('date',inplace=True)
        
        smaHigh = ta.sma(dfSSL['high'],length=10)
        smaLow = ta.sma(dfSSL['low'],length=10)
        current_candle_close = dfSSL.iloc[-1]['close']
        current_smaHigh = smaHigh.iloc[-1]
        current_smaLow = smaLow.iloc[-1]
        
        if current_candle_close > current_smaHigh:
            Hlv = 1
        if current_candle_close < current_smaLow:
            Hlv = -1
    except:
        print("Error SSL")
    time.sleep(1)
    pass

    

def is_bearish_candlestick(candle):
    return candle['close'] < candle['open']

def is_bullish_engulfing():
    if is_bearish_candlestick(previous_candle)\
    and float(current_candle['close']) > float(previous_candle['open']) \
    and float(current_candle['open']) <= float(previous_candle['close']) :
        print("Bullish Engulfing",datetime.datetime.now()+timedelta(minutes = -1))
    return True

def is_bearish_engulfing():
    if not is_bearish_candlestick(previous_candle)\
    and float(current_candle['close']) < float(previous_candle['open']) \
    and float(current_candle['open']) >= float(previous_candle['close']) :
        print("Bearish Engulfing", datetime.datetime.now()+timedelta(minutes = -1))
    return True

def take_profitloss(purchase_price,current_candle):
    balance = r.get_balance()
    dfb = pd.DataFrame(balance,columns=['type','exchange','currency','amount','available'])
    mybalanceusd = float(dfb.loc[dfb['currency']=='USD','available'])
    orderbook = r.get_current_order_book(ticker_g)
    
    if purchase_price * 1.02 == current_candle['high']:    #2% Profit
        sell_price = orderbook['asks'][0]['price']
        unit = mybalanceusd / float(sell_price)
        unit = round(unit,5)-0.00001
        unit = str(unit)
        #r.new_order(ticker_g,unit,current_candle['high'],"sell",["immediate-or-cancel"])
        print("Took Profit", datetime.datetime.now()+timedelta(minutes = -1),"  @  ",current_candle['high'])

    if purchase_price - 0.99 == current_candle['low']:     #1% Loss
        sell_price = orderbook['asks'][0]['price']
        unit = mybalanceusd / float(sell_price)
        unit = round(unit,5)-0.00001
        unit = str(unit)
        #r.new_order(ticker_g,unit,current_candle['low'],"sell",["immediate-or-cancel"])
        print("Took Loss", datetime.datetime.now()+timedelta(minutes = -1),"  @  ",current_candle['low'])

while True:
    try:
        ssl_ohlcv = gemini.fetch_ohlcv(ticker,timeframe='1h')
        dfSSL = pd.DataFrame(ssl_ohlcv, columns=['date','open','high','low','close','volume'])
        dfSSL['date'] = pd.to_datetime(dfSSL['date'], unit='ms')
        dfSSL['date'] = dfSSL['date'] + datetime.timedelta(hours=-4)
        dfSSL.set_index('date',inplace=True)
        
        smaHigh = ta.sma(dfSSL['high'],length=10)
        smaLow = ta.sma(dfSSL['low'],length=10)
        current_candle_close = dfSSL.iloc[-1]['close']
        current_smaHigh = smaHigh.iloc[-1]
        current_smaLow = smaLow.iloc[-1]
        
        ema_ohlcv = gemini.fetch_ohlcv(ticker,timeframe='5m')
        dfEMA = pd.DataFrame(ema_ohlcv, columns =['date','open','high','low','close','volume'])
    
        previous_candle = dfEMA.iloc[-3]
        current_candle = dfEMA.iloc[-2]
        
            
        if current_candle_close > current_smaHigh:
            #Testing SSL Up & Bull
            if is_bearish_candlestick(previous_candle)\
                and float(current_candle['close']) > float(previous_candle['open']) \
                and float(current_candle['open']) <= float(previous_candle['close']) \
                and float(current_candle['low'])<float(emaClose.iloc[-2])<float(current_candle['high']):
                    current_candle['close']
                    balance = r.get_balance()
                    dfb = pd.DataFrame(balance,columns=['type','exchange','currency','amount','available'])
                    mybalanceusd = float(dfb.loc[dfb['currency']=='USD','available'])
                    mybalancecoin = float(dfb.loc[dfb['currency']=='BTC','available'])
                    orderbook = r.get_current_order_book(ticker_g)
                    long_buy_price = orderbook['asks'][0]['price']
                    long_sell_price = orderbook['bids'][0]['price']
                    # unit = mybalanceusd / float(long_buy_price)
                    # unit = round(unit,5)-0.00001
                    # unit = str(unit)
                    #r.new_order(ticker_g,unit,long_buy_price,"buy",["immediate-or-cancel"])
                    print("Long", datetime.datetime.now()+timedelta(minutes = -1),"  @  ",long_buy_price)
                    print("SSL Up Bullish Engulfing")
                    
        
        
            #Testing SSL UP & Bear
            if not is_bearish_candlestick(previous_candle)\
                and float(current_candle['close']) < float(previous_candle['open']) \
                and float(current_candle['open']) >= float(previous_candle['close']) :
                    print("SSL Up Bearish Engulfing", datetime.datetime.now()+timedelta(minutes = -1))
    
        if current_candle_close < current_smaLow:                     
            # Testing SSL Down & Bull
            if is_bearish_candlestick(previous_candle)\
                and float(current_candle['close']) > float(previous_candle['open']) \
                and float(current_candle['open']) <= float(previous_candle['close']) \
                and float(current_candle['open'])<float(emaClose.iloc[-2])<float(current_candle['close']):
                    print("SSL Down Bullish Engulfing",datetime.datetime.now()+timedelta(minutes = -1))
    
            #Testing SSL Down & Bear
            if not is_bearish_candlestick(previous_candle)\
                and float(current_candle['close']) < float(previous_candle['open']) \
                and float(current_candle['open']) >= float(previous_candle['close']) \
                and float(current_candle['high'])>float(emaClose.iloc[-2])>float(current_candle['low']):
                    current_candle['close']
                    balance = r.get_balance()
                    dfb = pd.DataFrame(balance,columns=['type','exchange','currency','amount','available'])
                    mybalanceusd = float(dfb.loc[dfb['currency']=='USD','available'])
                    orderbook = r.get_current_order_book(ticker_g)
                    short_sell_price = orderbook['bids'][0]['price']
                    short_buy_price = orderbook['asks'][0]['price']
                    unit = mybalanceusd / float(short_sell_price)
                    unit = round(unit,5)-0.00001
                    unit = str(unit)
                    #r.new_order(ticker_g,unit,short_sell_price,"buy",["immediate-or-cancel"])
                    print("Short", datetime.datetime.now()+timedelta(minutes = -1),"  @  ",short_sell_price)
                    print("SSL Down Bearish Engulfing",datetime.datetime.now()+timedelta(minutes = -1))
                    

                  
    except:
        print("Error")
        
    time.sleep(1)

# while True:
#     try:
#         if long_sell_price >= long_buy_price*1.025:
#             #r.new_order(ticker_g,mybalancecoin,sell_price,"sell",["immediate-or-cancel"])
#             print("Sold for profit  @", long_sell_price)
        
#         if long_sell_price <= long_buy_price*0.985:
#             #r.new_order(ticker_g,mybalancecoin,sell_price,"sell",["immediate-or-cancel"])
#             print("Sold for loss  @", long_sell_price)

#         # if short_buy_price <= short_sell_price/1.025:
#         #     #r.new_order(ticker_g,unit,sell_price,"sell",["immediate-or-cancel"])
#         #     print("Sold for profit  @", short_buy_price)
        
#         # if short_buy_price >= short_sell_price/0.985:
#         #     #r.new_order(ticker_g,unit,sell_price,"sell",["immediate-or-cancel"])
#         #     print("Sold for loss  @", short_buy_price)

#     except:
#         print("Error @ taking profit/loss")
        
        
#     time.sleep(1)
    