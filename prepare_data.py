import pandas as pd
from pandas import Series, DataFrame
import glob
import os
import numpy as np
pd.set_option("display.max_columns", None)
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

daily_prices["Close"] = daily_prices["Close"].replace(0, np.nan)


#**Investigation**
#Further investigation to see how many rows in Close have 0 and what those rows look like .
# print((daily_prices["Close"] == 0).sum()) #Which will now print out 0 bc i replaced 0 with np nan later on.
# print(daily_prices[daily_prices["Close"] == 0].head(36))

#Thought Process:
#Before just deleting these rows i should try to see if this could be intential. I'm pretty sure it's not intentional because of the runtime error im getting.
#Since the assignment specifically asks me to calculate log return, I want to assume the data is supposed to contain values that would allow the calculation to work properly.
#If it was intentional (I hope not) then ill further investigate the reason why they are present.

#**Investigation**
#Grab a couple rows surrounding the first row where Close is 0. And then give me some relevant detials.
print(daily_prices.loc[1338961:1338967, ["Date", "Ticker","Close"]])
#Output
#Seem to be getting this
#March 14th - > 14.25
#March 15th - > 0
#March 16th -> 13.50
#My conclusion is that the zeros are inconsistent values.

#**Solution**
#INstead of deleting the whole row of data where Close is = 0  we should just replace it with nan. Because some of the data in that row could still be useful.
daily_prices["Close"] = daily_prices["Close"].replace(0, np.nan)
#should now be 0
# print((daily_prices["Close"] == 0).sum())





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

#Final boss type
#The close-to-close historical volatility, using the formulas in the appendix, on a lookback window of 21 trading days (roughly one calendar month).
# I keep getting an error "RuntimeWarning: divide by zero encountered in log result = getattr(ufunc, method)(*inputs, **kwargs)""
# The missing values which are zero are probably interfering with my results must do further investigation. (Can use this in my analysis)

yesterdaysClose = daily_prices.groupby("Ticker")["Close"].shift(1)
daily_prices["Daily Log Return"] = np.log(daily_prices["Close"] / yesterdaysClose)
daily_prices["Historical Volatility"] = (daily_prices.groupby("Ticker")["Daily Log Return"].rolling(21).std().reset_index(level= 0, drop = True))



# ============================================================
# 5. Monthly Dollar Value Dataframe.
# ============================================================
#Need to grab/make month column which will also give us year to categorize month by
daily_prices["Month"] = daily_prices["Date"].dt.to_period("M")


monthly_dollar_volume = daily_prices.groupby(["Ticker", 'Month'])["Volume Traded"].sum().reset_index()

# print(monthly_dollar_volume.head(20))
# print(monthly_dollar_volume.shape)


# ============================================================
# 6. Extreme days Data Frame
# ============================================================
#Grab where the condition is True
extreme_days = daily_prices[daily_prices["Daily Percent Change"].abs() >= 20]
# print(extreme_days.head())
# print(extreme_days.shape)


# ============================================================
# 7. Penny Stocks data Frame
# ============================================================
#Get most recent row and then keep ones where close < 1 (Already sorted)
current_prices = daily_prices.groupby("Ticker").tail(1)
penny_stocks = current_prices[current_prices["Close"] < 1]

# print(penny_stocks.shape) #467 current penny stocks curr day is april 1st (interesting)
# print(penny_stocks.head())




# ============================================================
# Building my Ticker Dataframe
# ============================================================

tickers = pd.read_csv("raw_data/symbols_valid_meta.csv")

print(tickers.head())
print(tickers.shape)
tickers.info()


print(tickers["Symbol"].duplicated().sum())
#Trying to find anything weird to do with finanxial status since its the only one that did populate all the way. but looks good to me
print(tickers.groupby("Listing Exchange")["Financial Status"].count())
#Cant find much wrong with tickers I think it's fine to continue with it.



# ============================================================
# Save to Prepared data folder
# ============================================================

daily_prices.to_parquet("prepared_data/daily_prices.parquet", index=False)

tickers.to_parquet("prepared_data/tickers.parquet", index=False)

monthly_dollar_volume.to_parquet("prepared_data/monthly_dollar_volume.parquet",index=False)

extreme_days.to_parquet("prepared_data/extreme_days.parquet",index=False)

penny_stocks.to_parquet("prepared_data/penny_stocks.parquet",index=False)

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