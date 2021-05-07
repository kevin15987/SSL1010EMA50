# SSL1010EMA50

This method uses SSL and EMA to predict the best entry point. 

How this works:
- Look at SSL to identify whether the stock is treding upward or downward. For this, SSL channel should be used at period of 10 and should be monitored at 1hr time frame.
- After identifying the stock movement using SSL, use EMA50 line at 5 minute timeframe to locate the entry point:
  - If the stock is trending upward,
    - locate "bullish engulfing" candlestick where it "touches" the EMA50 line. 
    - The "close" of the green candle should be the entry point for a long position
    - I set my profit/loss ratio to 2:1 
  - If the stock is trending downward,
    - locate "bearish engulfing" candlestick where it "touches" the EMA50 line. 
    - The "close" of the green candle should be the entry point for a short position
    - I set my profit/loss ratio to 2:1 


## DISCLAIMER ##
I’m not a certified financial planner/advisor nor a certified financial analyst nor an economist nor a CPA nor an accountant nor a lawyer. I’m not a finance professional through formal education. Invest at your own risk!
