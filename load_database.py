import pandas as pd
import psycopg2
import pyarrow.parquet as pq

from io import StringIO


# ============================================================
# PostgreSQL Connection
# ============================================================

# Connect Python to the PostgreSQL database running through Docker
connection = psycopg2.connect(
    host="localhost",
    database="marketanalysis",
    user="username",
    password="password",
    port="5432"
)

# Cursor is used to send SQL commands from Python to PostgreSQL
cursor = connection.cursor()

print("Connected to PostgreSQL!")


# ============================================================
# Load Tickers
# ============================================================

tickers = pd.read_parquet("prepared_data/tickers.parquet")

# PostgreSQL needs its own table structure before we can copy
# the DataFrame data into it
create_tickers_table = """
CREATE TABLE IF NOT EXISTS tickers (
    nasdaq_traded TEXT,
    symbol TEXT PRIMARY KEY,
    security_name TEXT,
    listing_exchange TEXT,
    market_category TEXT,
    etf TEXT,
    round_lot_size FLOAT,
    test_issue TEXT,
    financial_status TEXT,
    cqs_symbol TEXT,
    nasdaq_symbol TEXT,
    nextshares TEXT
);
"""

cursor.execute(create_tickers_table)
connection.commit()

# Only load the data if the table is currently empty
cursor.execute("SELECT COUNT(*) FROM tickers;")
ticker_count = cursor.fetchone()[0]

if ticker_count == 0:
    # COPY cannot take the DataFrame directly, so temporarily turn it
    # into CSV-formatted data in memory for PostgreSQL to read
    buffer = StringIO()

    tickers.to_csv(
        buffer,
        index=False,
        header=False,
        na_rep="\\N"
    )

    # Go back to the beginning so PostgreSQL reads the entire buffer
    buffer.seek(0)

    copy_tickers = """
    COPY tickers (
        nasdaq_traded,
        symbol,
        security_name,
        listing_exchange,
        market_category,
        etf,
        round_lot_size,
        test_issue,
        financial_status,
        cqs_symbol,
        nasdaq_symbol,
        nextshares
    )
    FROM STDIN
    WITH (FORMAT CSV, NULL '\\N');
    """

    cursor.copy_expert(copy_tickers, buffer)
    connection.commit()

    print("Tickers loaded into PostgreSQL!")

else:
    print("Tickers already loaded. Skipping!")


# ============================================================
# Load Daily Prices
# ============================================================

# daily_prices is much larger than the other files, so PyArrow lets
# us work through its row groups instead of loading everything at once
daily_prices_file = pq.ParquetFile(
    "prepared_data/daily_prices.parquet"
)

create_daily_prices_table = """
CREATE TABLE IF NOT EXISTS daily_prices (
    date TIMESTAMP,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    adj_close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    ticker TEXT,
    daily_percent_change DOUBLE PRECISION,
    daily_return DOUBLE PRECISION,
    volume_traded DOUBLE PRECISION,
    difference_in_closes DOUBLE PRECISION,
    daily_log_return DOUBLE PRECISION,
    historical_volatility DOUBLE PRECISION,
    month TEXT
);
"""

cursor.execute(create_daily_prices_table)
connection.commit()

print("Daily prices table ready!")

# Check whether the daily price data has already been loaded
cursor.execute("SELECT COUNT(*) FROM daily_prices;")
daily_prices_count = cursor.fetchone()[0]

if daily_prices_count == 0:

    copy_daily_prices = """
    COPY daily_prices (
        date,
        open,
        high,
        low,
        close,
        adj_close,
        volume,
        ticker,
        daily_percent_change,
        daily_return,
        volume_traded,
        difference_in_closes,
        daily_log_return,
        historical_volatility,
        month
    )
    FROM STDIN
    WITH (FORMAT CSV, NULL '\\N');
    """

    # The Parquet file contains 27 row groups. Load them one at a time
    # so we do not try to hold all 28+ million rows in memory at once
    for i in range(daily_prices_file.num_row_groups):
        batch = daily_prices_file.read_row_group(i).to_pandas()

        print(f"Row group {i + 1}: {len(batch)} rows")

        buffer = StringIO()

        batch.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N"
        )

        buffer.seek(0)

        cursor.copy_expert(copy_daily_prices, buffer)
        connection.commit()

        print(f"Row group {i + 1} loaded!")

else:
    print("Daily prices already loaded. Skipping!")


# ============================================================
# Load Monthly Dollar Volume
# ============================================================

monthly_dollar_volume = pd.read_parquet(
    "prepared_data/monthly_dollar_volume.parquet"
)

create_monthly_dollar_volume_table = """
CREATE TABLE IF NOT EXISTS monthly_dollar_volume (
    ticker TEXT,
    month TEXT,
    volume_traded DOUBLE PRECISION
);
"""

cursor.execute(create_monthly_dollar_volume_table)
connection.commit()

# Check whether the data has already been loaded
cursor.execute("SELECT COUNT(*) FROM monthly_dollar_volume;")
monthly_count = cursor.fetchone()[0]

print("Monthly rows currently in database:", monthly_count)

if monthly_count == 0:
    buffer = StringIO()

    monthly_dollar_volume.to_csv(
        buffer,
        index=False,
        header=False,
        na_rep="\\N"
    )

    buffer.seek(0)

    copy_monthly = """
    COPY monthly_dollar_volume (
        ticker,
        month,
        volume_traded
    )
    FROM STDIN
    WITH (FORMAT CSV, NULL '\\N');
    """

    cursor.copy_expert(copy_monthly, buffer)
    connection.commit()

    print("Monthly dollar volume loaded into PostgreSQL!")

else:
    print("Monthly dollar volume already loaded. Skipping!")


# ============================================================
# Load Extreme Days
# ============================================================

extreme_days = pd.read_parquet(
    "prepared_data/extreme_days.parquet"
)

create_extreme_days_table = """
CREATE TABLE IF NOT EXISTS extreme_days (
    date TIMESTAMP,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    adj_close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    ticker TEXT,
    daily_percent_change DOUBLE PRECISION,
    daily_return DOUBLE PRECISION,
    volume_traded DOUBLE PRECISION,
    difference_in_closes DOUBLE PRECISION,
    daily_log_return DOUBLE PRECISION,
    historical_volatility DOUBLE PRECISION,
    month TEXT
);
"""

cursor.execute(create_extreme_days_table)
connection.commit()

# Check whether the data has already been loaded
cursor.execute("SELECT COUNT(*) FROM extreme_days;")
extreme_days_count = cursor.fetchone()[0]

print("Extreme days rows currently in database:", extreme_days_count)

if extreme_days_count == 0:
    buffer = StringIO()

    extreme_days.to_csv(
        buffer,
        index=False,
        header=False,
        na_rep="\\N"
    )

    buffer.seek(0)

    copy_extreme_days = """
    COPY extreme_days (
        date,
        open,
        high,
        low,
        close,
        adj_close,
        volume,
        ticker,
        daily_percent_change,
        daily_return,
        volume_traded,
        difference_in_closes,
        daily_log_return,
        historical_volatility,
        month
    )
    FROM STDIN
    WITH (FORMAT CSV, NULL '\\N');
    """

    cursor.copy_expert(copy_extreme_days, buffer)
    connection.commit()

    print("Extreme days loaded into PostgreSQL!")

else:
    print("Extreme days already loaded. Skipping!")


# ============================================================
# Load Penny Stocks
# ============================================================

penny_stocks = pd.read_parquet(
    "prepared_data/penny_stocks.parquet"
)

create_penny_stocks_table = """
CREATE TABLE IF NOT EXISTS penny_stocks (
    date TIMESTAMP,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    adj_close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    ticker TEXT,
    daily_percent_change DOUBLE PRECISION,
    daily_return DOUBLE PRECISION,
    volume_traded DOUBLE PRECISION,
    difference_in_closes DOUBLE PRECISION,
    daily_log_return DOUBLE PRECISION,
    historical_volatility DOUBLE PRECISION,
    month TEXT
);
"""

cursor.execute(create_penny_stocks_table)
connection.commit()

# Check whether the data has already been loaded
cursor.execute("SELECT COUNT(*) FROM penny_stocks;")
penny_stocks_count = cursor.fetchone()[0]

print("Penny stock rows currently in database:", penny_stocks_count)

if penny_stocks_count == 0:
    buffer = StringIO()

    penny_stocks.to_csv(
        buffer,
        index=False,
        header=False,
        na_rep="\\N"
    )

    buffer.seek(0)

    copy_penny_stocks = """
    COPY penny_stocks (
        date,
        open,
        high,
        low,
        close,
        adj_close,
        volume,
        ticker,
        daily_percent_change,
        daily_return,
        volume_traded,
        difference_in_closes,
        daily_log_return,
        historical_volatility,
        month
    )
    FROM STDIN
    WITH (FORMAT CSV, NULL '\\N');
    """

    cursor.copy_expert(copy_penny_stocks, buffer)
    connection.commit()

    print("Penny stocks loaded into PostgreSQL!")

else:
    print("Penny stocks already loaded. Skipping!")


# ============================================================
# Close Database Connection
# ============================================================

# Finished using PostgreSQL, so close everything cleanly
cursor.close()
connection.close()

print("PostgreSQL connection closed.")