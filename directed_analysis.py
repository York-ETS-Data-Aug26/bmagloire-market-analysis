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
returns_data = daily_prices.merge(tickers[["Symbol", "ETF"]],left_on="Ticker",right_on="Symbol",how="left")
print(returns_data[["Ticker", "Symbol", "ETF", "Daily Percent Change"]].head(50))
print(returns_data["ETF"].value_counts()) # N   24175924 stock daily price rows :  Y   3950926 ETF daily price rows


#Trying to find something concrete
#Found that somehow mean is above 100%? and median is 0? Definitly some outliers going on.
return_summary = (returns_data.groupby("ETF")["Daily Percent Change"].agg(["count", "mean", "median", "std"]))
print(return_summary)
#Looking for outliers
print(returns_data["Daily Percent Change"].describe())#I have a max of 123,833,300%

#Find the row responsible
max_return = returns_data["Daily Percent Change"].max()
max_return_row = returns_data[returns_data["Daily Percent Change"] == max_return]
print(max_return_row)

#Now we know that the symbol SAFis responsible so deeper analysis could be made here.



# ============================================================
# 2.If I had $1,000 to invest?
# ============================================================


# ============================================================
# 3.Where is there missing or invalid data in this dataset?
# ============================================================

print(daily_prices.isnull().sum())
# Check data types
print(daily_prices.dtypes)
