
NASDAQ Market Analysis Report

##Overview
The goal of this project was to take raw NASDAQ stock and etf data, clean it up, organize it into usable dataframes and run analysis on those dataframes to come
up with certain conclusions. The raw data came out to thousands of individual CSV files for both stocks and ETF's, alone with one metadata file containing more
information about each ticker. My main goal was to try to understand the Assessment at a high level, focus on formatting my code and files, learn how to clean and 
merge data, and finally make some type of conclusions about said data. I believe I got through a lot of what I wanted to, but still fell short not completing the 
analysis. However, I am happy with how i structured/organized my data


##Project Structure

bmagloire-market-analysis/
│
├── raw_data/
│   ├── stocks/
│   ├── etfs/
│   └── symbols_valid_meta.csv
│
├── prepared_data/
│
│
├── prepare_data.py
├── directed_analysis.py
├── report.md
├── README.md
└── .gitignore


##Running the project
First install require packages:
- pip install pandas 
- pip install numpy
- pip install pyarrow


Run my prepare_data.py first which will then create the 5 parquet files and then my analysis is available in Report, but i tried my best to also leave detailed
comments. Open to criticism.