# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def main():
    goldetf_ticker = "1540.T"
    goldetf = yf.Ticker(goldetf_ticker)
    goldetf_price = goldetf.history(period="1d")["Close"].iloc[-1]
    goldinfo = goldetf.info
    goldnav = goldinfo.get("navPrice")

    if goldnav is None:
        print("NAV情報が取得できませんでした。")
        return

    gold_deviation = (goldetf_price - goldnav) / goldnav * 100

    # CSVに追記
    data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "etf_price": goldetf_price,
        "nav": goldnav,
        "deviation(%)": gold_deviation
    }
    df_new = pd.DataFrame([data])

    filename = "gold_deviation_log.csv"
    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(filename, index=False)
    print(df_new)

if __name__ == "__main__":
    main()
