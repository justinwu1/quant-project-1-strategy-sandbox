import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os 
import json

ticker = yf.Ticker("AAPL")


def get_cache_file(cache_file="cache.json"):
    # if file exists, return the file
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            return json.load(file)
    return {}

def save_cache_file(cache_file,data):
    with open(cache_file,"w") as file:
        json.dump(data,file)

def download_stock(ticker,start_date,end_date,interval="1d",cache_file="cache.json"):
    cache = get_cache_file(cache_file)
    if ticker in cache:
        print("Using Cached Data")
        return pd.DataFrame(cache[ticker])
    else:
        print("Downloading Data")
        stock = yf.Ticker(ticker)
        stock_history = stock.history(start=start_date, end=end_date, interval=interval)
        stock_history.index = stock_history.index.astype(str)
        cache[ticker] = stock_history.to_dict()
        save_cache_file(cache_file,cache)
        return stock_history

df = download_stock("AAPL","2020-01-01","2020-12-31")
print(df.head())
