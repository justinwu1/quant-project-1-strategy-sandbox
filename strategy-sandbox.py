import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os 
import json

ticker = yf.Ticker("AAPL")

# Helper function for downloading stock data
def get_cache_file(cache_file="cache.json"):
    # if file exists, return the file
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            return json.load(file)
    return {}
# Helper function for saving stock data
def save_cache_file(cache_file,data):
    with open(cache_file,"w") as file:
        json.dump(data,file)

def download_stock(ticker, start_date, end_date, interval="1d", cache_file="cache.json"):
    # Validation for start and end date
    if pd.to_datetime(start_date) > pd.to_datetime(end_date):
        raise ValueError("Start date must be before end date")

    # Create cache key using ticker + range
    key = f"{ticker}_{start_date}_{end_date}_{interval}"
    cache = get_cache_file(cache_file)

    if key in cache:
        print(f"✅ Using Cached Data for: {key}")
        return pd.DataFrame(cache[key])

    # Download from yfinance
    print(f"⬇️ Downloading Data for: {key}")
    stock = yf.Ticker(ticker)
    stock_history = stock.history(start=start_date, end=end_date, interval=interval)

    if stock_history.empty:
        print("⚠️ No data found for the given ticker and date range")
        return stock_history

    stock_history.index = stock_history.index.astype(str)
    cache[key] = stock_history.to_dict()
    save_cache_file(cache_file, cache)
    return stock_history


# Removes duplicates, fill forward and backward gap, drop rows with NaN values.
def clean_stock_data(df:pd.DataFrame)->pd.DataFrame:
    # Clear duplicate 
    df = df[~df.index.duplicated(keep="first")]
    # Fill forward and Backward
    df.bfill(inplace=True)
    df.ffill(inplace=True)
    
    # Drop rows with NaN values
    df = df.dropna(how="all",)
    return df

df = download_stock("AAPL","2025-05-25","2025-05-28")
df = clean_stock_data(df)
print(df)
