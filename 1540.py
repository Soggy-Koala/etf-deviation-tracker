# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def main():
    # --- 銘柄リスト ---
    tickers = {
        "1540.T": "Gold"
    }

    usd_jpy = yf.Ticker("JPY=X").history(period="1d")["Close"].iloc[-1]

    data = []
    for ticker, name in tickers.items():
        t = yf.Ticker(ticker)
        price = t.history(period="1d")["Close"].iloc[-1]
        nav = t.info.get("navPrice")

        if nav:
            nav_jpy = nav
            deviation = (price - nav_jpy) / nav_jpy * 100
        else:
            nav_jpy = None
            deviation = None

        data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ticker": ticker,
            "name": name,
            "price": price,
            "nav_jpy": nav_jpy,
            "deviation_pct": deviation
        })

    # --- CSVファイル名 ---
    csv_filename = "1540.csv"
    png_filename = "1540.png"

    # --- CSV追記 ---
    df_new = pd.DataFrame(data)
    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    # timestamp列をdatetime型に変換
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values("timestamp", inplace=True)

    df_all.to_csv(csv_filename, index=False)

    # --- プロット ---
    plt.figure(figsize=(10, 8))
    colors = {
        "Gold": "gold"#,
        #"Silver": "gray"#,
        #"Platinum": "purple",
        #"Palladium": "brown",
        #"RoyalMetal": "orange"
    }

    for name in tickers.values():
        df_sub = df_all[df_all["name"] == name]
        if df_sub.empty:
            continue

        # ETF実線・NAV点線を描画（データが1点ならプロット）
        plt.plot(df_sub["timestamp"], df_sub["price"], label=f"{name} ETF", color=colors[name], linestyle="-", marker="o")
        if df_sub["nav_jpy"].notna().any():
            plt.plot(df_sub["timestamp"], df_sub["nav_jpy"], label=f"{name} NAV", color=colors[name], linestyle="--", marker="x")

    plt.xlabel("Time (JST)")
    plt.ylabel("Price / NAV (JPY)")
    plt.title("ETF vs NAV (1540)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_filename)
    plt.close()

    # --- 最新乖離率を表示 ---
    for row in data:
        print(f"{row['name']} ({row['ticker']}) ETF%NAV: {row['deviation_pct']:.2f}%")

    print(f"✅ Data appended to {csv_filename}")
    print(f"✅ Chart updated: {png_filename}")


if __name__ == "__main__":
    main()
