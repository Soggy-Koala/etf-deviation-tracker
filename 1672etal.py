# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def main():
    # --- 銘柄リスト ---
    tickers = {
        "1672.T": "Gold",
        "1673.T": "Silver",
        "1674.T": "Platinum",
        "1675.T": "Palladium"
    }

    # --- USD/JPY 為替レートを取得 ---
    usd_jpy = yf.Ticker("JPY=X").history(period="1d")["Close"].iloc[-1]

    data = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- 各ETFのデータを取得 ---
    for ticker, name in tickers.items():
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if hist.empty:
            print(f"⚠️ No data for {ticker}")
            continue

        price = hist["Close"].iloc[-1]
        nav = t.info.get("navPrice")

        if nav:
            nav_jpy = nav * usd_jpy
            deviation = (price - nav_jpy) / nav_jpy * 100
        else:
            nav_jpy = None
            deviation = None

        data.append({
            "timestamp": now,
            "ticker": ticker,
            "name": name,
            "price": price,
            "nav_jpy": nav_jpy,
            "deviation_pct": deviation
        })

    # --- CSV追記 ---
    csv_filename = "1672etal.csv"
    df_new = pd.DataFrame(data)

    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(cs
