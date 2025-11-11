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

    # --- 為替 ---
    usd_jpy = yf.Ticker("JPY=X").history(period="1d")["Close"].iloc[-1]

    data = []
    for ticker, name in tickers.items():
        t = yf.Ticker(ticker)
        price = t.history(period="1d")["Close"].iloc[-1]
        nav = t.info.get("navPrice")

        if nav:
            nav_jpy = nav * usd_jpy
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

    # --- CSVファイル ---
    csv_filename = "1672etal.csv"
    df_new = pd.DataFrame(data)

    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    # timestamp列をdatetime型に変換 & ソート
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values("timestamp", inplace=True)

    # CSVに保存
    df_all.to_csv(csv_filename, index=False)
    print(f"✅ Data appended to {csv_filename}")

    # --- グラフ作成（各銘柄ごと） ---
    colors = {
        "Gold": "gold",
        "Silver": "gray",
        "Platinum": "purple",
        "Palladium": "brown"
    }

    for name in tickers.values():
        df_sub = df_all[df_all["name"] == name]
        if df_sub.empty:
            continue

        plt.figure(figsize=(10, 6))
        # ETF実線
        plt.plot(df_sub["timestamp"], df_sub["price"],
                 label=f"{name} ETF", color=colors[name], linestyle="-", marker="o")
        # NAV点線
        if df_sub["nav_jpy"].notna().any():
            plt.plot(df_sub["timestamp"], df_sub["nav_jpy"],
                     label=f"{name} NAV", color=colors[name], linestyle="--", marker="x")

        # 最新乖離率をグラフ上に表示
        latest_dev = df_sub["deviation_pct"].iloc[-1]
        plt.text(df_sub["timestamp"].iloc[-1],
                 df_sub["price"].iloc[-1],
                 f"{latest_dev:.2f}%", color=colors[name], fontsize=10,
                 ha="left", va="bottom")

        plt.xlabel("Time (JST)")
        plt.ylabel("Price / NAV (JPY)")
        plt.title(f"ETF vs NAV ({name})")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()

        # 銘柄ごとにPNG保存
        png_filename = f"{name}.png"
        plt.savefig(png_filename)
        plt.close()
        print(f"✅ Chart updated: {png_filename}")

    # --- 最新乖離率をコンソールに表示 ---
    for row in data:
        dev = row['deviation_pct']
        if dev is not None:
            print(f"{row['name']} ({row['ticker']}) ETF%NAV: {dev:.2f}%")
        else:
            print(f"{row['name']} ({row['ticker']}) ETF%NAV: N/A")

if __name__ == "__main__":
    main()
