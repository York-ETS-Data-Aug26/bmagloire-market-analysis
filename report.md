#NASDAQ Market Analysis Report

##Overview
The goal of this project was to take raw NASDAQ stock and etf data, clean it up, organize it into usable dataframes and run analysis on those dataframes to come
up with certain conclusions. The raw data came out to thousands of individual CSV files for both stocks and ETF's, alone with one metadata file containing more
information about each ticker. My main goal was to try to understand the Assessment at a high level, focus on formatting my code and files, learn how to clean and 
merge data, and finally make some type of conclusions about said data. I believe I got through a lot of what I wanted to, but still fell short not completing the 
analysis.

---

##Data Prep

I first found all of the stock and ETF CSV files using 'glob'. Each file only contained the price data, so I used the file name ticker symbol for each DataFrame
. For example, 'AAPL.csv' became ticker 'AAPL'. After that i combined all stock files together, comined all ETF fiels together, and then combined both of those into one 
'daily_prices 'DataFrame. The final daily price dataset contians over 28 million rows. I also created a separate tickers DataFrame using the metadata file. Couldn't
really find toom uch invalid or missleading information so i went on.


##Derived Fields
I added the following fields to 'daily_prices':
- Daily Percent Change
- Daily Return in dollars
- Dollar Volume Traded
- Difference between Adjusted Close and Close
- Daily Log Return
- 21-day Historical Volatility

I also created additional DataFrames:
- Monthly Dollar Volume
- Extreme Days
- Current Penny Stocks


---

##Data Cleaning

One issue I found early was that some values in the 'Close' column were equal to zero. At first I was not sure if those values were intentional, 
so I looked at the rows around one of the zero values to see if the data was it was uniform.
For example, for ticker APEX:

- March 14: Close = 14.25
- March 15: Close = 0
- March 16: Close = 13.50

0 is odd here and doesnt make any sense based on surrounding values. The zero values were also causing problems when calculating log returns because
dividing by zero created invalid results. Instead of deleting the entire row, I replaced only the zero value in 'Close' with 'NaN'.
This kept the rest of the row available in case the other values were still useful. There were 36 zero closing prices found.

---

##Directed Analysis

###1. Stock vs ETF Daily Returns

To compare stock and ETF daily returns, I first connected the daily price data with the ticker metadata. The 'daily_prices' DataFrame had teh faily percent
change, while the 'tickers' DataFrame had teh information showing whetehr the ticker was stock or an ETF. Merged the two using the ticker symbol and printed
the results:
- 24,175,924 stock daily price rows
- 3,950,926 ETF daily price rows

I then grouped the data by the ETF indicator and calculated for count, mean, median, and std of hte daily pct change.

The results were:

| Type | Count | Mean | Median | Standard Deviation |
| --- | ---: | ---: | ---: | ---: |
| Stocks | 24,168,974 | 134.69% | 0.00% | 42,760.13% |
| ETFs | 3,948,717 | 100.14% | 0.00% | 27,296.43% |

At first these results looked very strange because an average daily return above 100% does not make sense as a normal result. Noticed the max value was 
123,833,200%. Found the row responsible for the max value which was 'SAF'on Decemeber 10 , 2004. Because of extreme vlaues like this, the mean and std are clearly
being affected by outliers. The median was also 0% which should further prove my skepticism on the validity of the data. In conclusion based on the raw results,
stocks had a higher spread in returns than ETF's, but i would not consider the mean values reliable without doing more investigating or handling  of extreme values.


---

###3. Missing and Invalid Data

I checked and prepared the dataset for missing values and datatypes. The original raw price data had 683 missing values in 

- Open
- High
- Low
- Close
- Adjusted Close
- Volume

After replacing the 36 invalid zero closing prices with 'NaN', the total number of missing values increased to 718. Some derived fields had more missing values 
as a result which is expected becasue some require a previous day's closing price. Because of that tge first row for eah ticker cannot have one of those values.
Historical Volatility had even more missing values because it requires a full 21-day rolling window before it can be calculated.

The prepared dataset used the following data types:

- Date: datetime
- Price and volume fields: numeric
- Ticker: string
- Month: monthly period


Because of the time straint I did not find any major data type problems after the preparation process. I feel as though with extra time i couldve gone back and 
did analysis on every missing trading date, including separating expected weekends and holidays from unexpected missing dates. This was the extent to which
I got during this assessment.













