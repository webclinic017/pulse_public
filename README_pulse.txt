This is a collection of scripts I created for downloading and backtesting US stocks data.
1. bat scripts are for daily downloads. launch append_1 and append_d
2. calc_5, calc_d and calc_intraday are for searching for patterns
3. classes are inherited from Interactive Brokers Python API classes it ships with
4. conditions are helper functions to express search conditions
5. func are functions to transform arrays, add indicators and other data, normalize raw data and test final data
6. correct.py takes both daily and 1min arrays, removes duplicates and makes sure the days match. Uses tests from the func.py file
6.1 checks if each day is 540 candles long
6.2 checks if each day starts with 700am
6.3 splits 2d array of 1min candles into 3d arrays of days of 1min candles and checks if dates match with daily candles
7. get_1min_corr uses daily candles as a template and downloads and normalizes 1 day of 1min candles per cycle. All the search functions are written in numpy, hence we heavily depend on the arrays being symmetrical. Pre market data is anything but. It can start at 4 or at 7 or at 8 depending on how much volume is traded on average. It can miss candles. Missed candles may or may not be masked. correct_1day() function uses the imported template to normalize the raw data minute by minute. If this minute is present in the data, it copies it as the mask and skips it. If the minute is absent, it masks it.
8. real time scan for Interactive Brokers TWS API. Works paired with the desktop TWS platform.
Downloads 5min candles at ~50requests per second + waiting time. Timeframe can be reduced down to 1-2min at the expense of reducing the number of stocks. So far it handles 70+ stocks per 3-4sec no problem.
For display purposes, it just prints out values for each stock from the dictionary it populates during the day and adds volume weighted average price. We can add any indicator we want and print out only matches, which is how it normally works on my machine.
This scanner can handle difficulties with the internet connection - after losing the connection and restoring it, "picks up the slack", downloads missing data once every 2sec and then returns to the normal mode of requesting data every 5min.
Their servers arent very reliable.
9. send order is a helper script to send orders faster. Each clientID is the number of microseconds currently elapsed since the beginning of the current second, highly unlikely they will ever match, so it can be used with scanner or any other similar tools (IBKR require unique connectID). Supports market, limit and conditions orders for stocks and stock options.
Accepts string like
aapl b 100 mkt
aapl b 100 lmt 145.60
aapl.150.c.20221021 b 1 mkt 
aapl.150.c.20221021 b 1 mkt if spy > 380