import pandas as pd
from pandas import Series, DataFrame
import glob
import os
import numpy as np
# ============================================================
# 1. FILE PATH Stuff
# ============================================================

#Finds all stock csv files.
stock_file_path = "raw_data/stocks/*.csv"
stock_files = glob.glob(stock_file_path)

#Finds all ETF csv files.
etf_file_path = "raw_data/etfs/*.csv"
etf_files = glob.glob(etf_file_path)

# ============================================================
# 2. BUILD DAILY PRICES DataFrame
# ============================================================

#-------Stocks-----
stock_dataframes = []

#Take one of the file paths from stock files - > read it -> then append to list
for file in stock_files:
    df = pd.read_csv(file)

    #Extracts the basename of the file so for exmaple AAPL.csv but now we must get rid of the csv by doing the splittext method.
    ticker = os.path.basename(file)
    ticker = os.path.splitext(ticker)[0]

    #Create the ticker column
    df["Ticker"] = ticker

    #Appends to list
    stock_dataframes.append(df)
#Combine all stock DataFrames into one DataFrame that we will combine later.
stocks_df = pd.concat(stock_dataframes, ignore_index=True)

#---------ETFS--------

#Repeat for ETF's
etf_dataframes = []
for file in etf_files:
    df= pd.read_csv(file)

    #Extracts the basename of the file so for example AAPL.csv, but now we must get rid of the csv by doing the split text method.

    ticker = os.path.basename(file)
    ticker = os.path.splitext(ticker)[0]

    #Create the ticker cloumn
    df["Ticker"] = ticker

    #Append to the list
    etf_dataframes.append(df)

#Combine all ETF DataFrames into one DataFrame that we will combine later.
etfs_df = pd.concat(etf_dataframes, ignore_index=True)

#-------Combine--------

#Combine both made dataframes into finally my daily prices.
daily_prices = pd.concat([stocks_df, etfs_df], ignore_index=True)



# ============================================================
# 3. CLEAN DAILY PRICES
# ============================================================

#Date column is a string turning it into a time
daily_prices["Date"] = pd.to_datetime(daily_prices["Date"])
#Make sure rows are sorted
daily_prices = daily_prices.sort_values(by=["Ticker", "Date"])

#Going to first see what or why something is missing and seeing if i can draw any conclusions.
# missing_rows = daily_prices[daily_prices["Close"].isna()] #Pandas will keep the rows where the condition is true.
# print(missing_rows.head(20))
# print(missing_rows.shape)



# print(daily_prices.head(20))
# ============================================================
# 4. ADD DERIVED DAILY PRICE FIELDS
# ============================================================

#The percent daily change in the close price (close-to-close).
#Add another column that gives close to close changes. We have to group by ticker so that it restarts per ticker. and then maniupulate the column we made by using the close colum.
daily_prices["Daily Percent Change"] = daily_prices.groupby("Ticker")["Close"].pct_change() * 100

#
#The daily return in dollars (today's close minus yesterday's close).
daily_prices["Daily Return"] = daily_prices["Close"] - daily_prices.groupby("Ticker")["Close"].shift(1)

#The dollar volume traded that day (close × volume).
# Grab the Volume. Don't need groupby because both numbers we are comparing are in the same row.
daily_prices["Volume Traded"] = daily_prices["Close"] * daily_prices["Volume"]

#The difference between the adjusted close and the close.
#
daily_prices["Difference in closes"] = daily_prices["Adj Close"] - daily_prices["Close"]

#Final Boss
#The close-to-close historical volatility, using the formulas in the appendix, on a lookback window of 21 trading days (roughly one calendar month).
#

yesterdaysClose = daily_prices.groupby("Ticker")["Close"].shift(1)

daily_prices["Daily Log Return"] = np.log(daily_prices["Close"] / yesterdaysClose)

daily_prices["Historical Volatility"] = (daily_prices.groupby("Ticker")["Daily Log Return"].rolling(21).std().reset_index(level= 0, drop = True))
print(daily_prices.head(25))




















# ============================================================
# 5. BUILD TICKERS DATAFRAME
# ============================================================



# ============================================================
# 6. BUILD DERIVED DATAFRAMES
# ============================================================



# ============================================================
# 7. SAVE PREPARED DATA TO PARQUET
# ============================================================























# ============================================================
# TESTING / Debugging area
# ============================================================


'''
Testing commands:
#Takes like a full minute to print.
# print(len(stock_files))
# print(len(etf_files))
# print(daily_prices.head()) #Looks good enough prints the first 5 tickers starting with A
# print(daily_prices.shape) #28148368

#--------

# print(daily_prices.info())
# print(daily_prices.isna().sum())
OUTPUT:

# RangeIndex: 28148368 entries, 0 to 28148367
# Data columns (total 8 columns):
 #   Column     Dtype  
---  ------     -----  
#  0   Date       str    #Gonna have to change this with pd.to_datetime eventually.
#  1   Open       float64 
#  2   High       float64
#  3   Low        float64
#  4   Close      float64
#  5   Adj Close  float64
#  6   Volume     float64 
#  7   Ticker     str    
# dtypes: float64(6), str(2)
# memory usage: 2.0 GB
# None
# Date           0
# Open         683 #Interesting to note that all coluimns have exactly 683 missing values.
# High         683
# Low          683
# Close        683
# Adj Close    683
# Volume       683
# Ticker         0
# dtype: int64
'''