import pandas as pd
pd.set_option("display.max_rows", None)
# ============================================================
# Load Prepared Data
# ============================================================
daily_prices = pd.read_parquet("prepared_data/daily_prices.parquet")
tickers = pd.read_parquet("prepared_data/tickers.parquet")
#Doesn't take long to print anymore thank god.
# print(daily_prices.shape)
# print(tickers.shape)

# ============================================================
# 1.Stock vs ETF daily returns?
# ============================================================
#
# returns_data = daily_prices.merge(tickers[["Symbol", "ETF"]],left_on="Ticker",right_on="Symbol",how="left")
# print(returns_data[["Ticker", "Symbol", "ETF", "Daily Percent Change"]].head(50))
# print(returns_data["ETF"].value_counts()) # N   24175924 stock daily price rows :  Y   3950926 ETF daily price rows
#
#
# #Trying to find something concrete
# #Found that somehow mean is above 100%? and median is 0? Definitly some outliers going on.
# return_summary = (returns_data.groupby("ETF")["Daily Percent Change"].agg(["count", "mean", "median", "std"]))
# print(return_summary)
# #Looking for outliers
# print(returns_data["Daily Percent Change"].describe())#I have a max of 123,833,300%
#
# #Find the row responsible
# max_return = returns_data["Daily Percent Change"].max()
# max_return_row = returns_data[returns_data["Daily Percent Change"] == max_return]
# print(max_return_row)

#Now we know that the symbol SAFis responsible so deeper analysis could be made here.



# ============================================================
# 2.If you had $1,000 to invest on April 3rd, 2000 (the first trading day of that month),
# what would have been the best stock to invest in, and what would that investment be worth on April 1st, 2020 (the last trading day in the dataset)? Repeat this for ETFs.
# ============================================================
# start_date = daily_prices[daily_prices["Date"] == "2000-04-03"]
#
# end_date = daily_prices[daily_prices["Date"] == "2020-04-01"]
#
# investment_data = start_date[["Ticker", "Close"]].merge(
#     end_date[["Ticker", "Close"]],
#     on="Ticker",
#     how="inner",
#     suffixes=("_2000", "_2020")
# )
#
# print(investment_data.head())
#
# investment_data["Shares"] = 1000 / investment_data["Close_2000"]
# investment_data["Final Value"] = (investment_data["Shares"] * investment_data["Close_2020"])
#
# investment_data = investment_data.merge(
#     tickers[["Symbol","ETF"]],
#     left_on="Ticker",
#     right_on="Symbol",
#     how="left"
# )
#
# stocks = investment_data[investment_data["ETF"] == "N"]
# etfs = investment_data[investment_data["ETF"] == "Y"]
#
# best_stock = stocks.loc[stocks["Final Value"].idxmax()]
# best_etf = etfs.loc[etfs["Final Value"].idxmax()]
#
# print("Best Stock: ", best_stock)
# print("Best ETF: ", best_etf)

#The best stock is MNST
#The best etf is COM


# ============================================================
# 3.Where is there missing or invalid data in this dataset? Include missing dates, data type mismatches, and values that do not make sense.
# For missing dates specifically, flag whether the missing date is expected (weekends, market holidays) or unexpected.
# ============================================================
# print("\nMissing Values:")
# print(daily_prices.isna().sum())
#
#
# missing_in_close = daily_prices[daily_prices["Close"].isna()]
#
# print("\nRows With Missing Close:")
# print(missing_in_close.head(20))
# print("Total:", missing_in_close.shape[0])
#
#
# #**
# #Shows what dates are producing the most of these missing price rows.
# print(missing_in_close["Date"].value_counts().head(20))
#
# # 2001-09-12    67
# # 2012-10-29    28
# # 2020-04-02    20
# # 2001-09-13    12
# # 2018-12-05    11
# # 1995-05-29     9
# # 2001-09-11     8
# # 1996-11-28     7
#
#
# #After the data preparation no inappropriate data types were identified. Everything looks good.
# print("\nData Types:")
# print(daily_prices.dtypes)
#
#
# #Check for 0's in close shouldnt be any becasue of my replace in my prepare data file.
# zero_close = daily_prices[daily_prices["Close"] == 0]
#
# print("\nZero Close Prices:")
# print(zero_close[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]].head(20))
# print("Total:", zero_close.shape[0])
#
# #Check for negative values
# print("\nNegative Values:")
# print("Open:", (daily_prices["Open"] < 0).sum())
# print("High:", (daily_prices["High"] < 0).sum())
# print("Low:", (daily_prices["Low"] < 0).sum())
# print("Close:", (daily_prices["Close"] < 0).sum())
# print("Adj Close:", (daily_prices["Adj Close"] < 0).sum()) #only negative.
# print("Volume:", (daily_prices["Volume"] < 0).sum())



# ============================================================
# 4.Which stocks have strange close vs. adjusted close values? Consider rows where the difference between the two is greater than 25%. Explain what is driving those differences.
# ============================================================


# daily_prices["Close Adj Percent Difference"] = (abs(daily_prices["Difference in closes"])/ daily_prices["Close"]) * 100
#
# print(daily_prices[["Ticker", "Close", "Adj Close", "Close Adj Percent Difference"]].head(20))
#
#
# strange_closes = daily_prices[daily_prices["Close Adj Percent Difference"] > 25]
#
# print(strange_closes[["Date", "Ticker", "Close", "Adj Close", "Close Adj Percent Difference"]].head(20))
# print("Total strange rows:", strange_closes.shape[0]) #Over 9 million rows are strange
#
#
#
# #Shows that ticker with the most trading days where the difffernce was greater than 25%.
# strange_tickers = (strange_closes["Ticker"].value_counts().head(20))
# print(strange_tickers)



# ============================================================
# 5. Which tickers had the most extreme days? What were the most extreme days in the market overall?
# ============================================================

# extreme_days = daily_prices[abs(daily_prices["Daily Percent Change"]) >= 20]
# #Top 20 extreme days
# print(extreme_days[["Date", "Ticker", "Close", "Daily Percent Change"]].head(20))
# print("Total extreme days:", extreme_days.shape[0])
#
# #Shows the top ten extreme days.
# most_extreme_tickers = extreme_days["Ticker"].value_counts().head(10)# PBC is the highest.
# print(most_extreme_tickers)
#
# #Shows what the most extreme days in the market overall were.
# extreme_market_days = extreme_days["Date"].value_counts().head(10) # 2020-03-18 is the highest
# print(extreme_market_days)

# ============================================================
# 6. Which 5 tickers are the most and least volatile over time, using the volatility measure above? Note how sensitive that ranking is to the lookback window and to the time period you measure over.
# ============================================================

ticker_volatility = (daily_prices.groupby("Ticker")["Historical Volatility"].mean())
print(ticker_volatility.head())

#Prints the 5 most and least volatile ticker
most_volatile = ticker_volatility.nlargest(5)
least_volatile = ticker_volatility.nsmallest(5)
print("5 Most Volatile:")
print(most_volatile)
print("\n5 Least Volatile:")
print(least_volatile)


#Prints the 5 most and least volatile ticker with a different lookback window.

daily_prices["60 Day Volatility"] = (daily_prices.groupby("Ticker")["Daily Log Return"].rolling(60).std().reset_index(level=0, drop=True))

ticker_volatility_60 = (daily_prices.groupby("Ticker")["60 Day Volatility"].mean()
                        )
most_volatile_60 = ticker_volatility_60.nlargest(5)
least_volatile_60 = ticker_volatility_60.nsmallest(5)

print("60-Day Most Volatile:")
print(most_volatile_60)
print("\n60-Day Least Volatile:")
print(least_volatile_60)

#Not very sensitive rankings stayed teh same for the most part.




