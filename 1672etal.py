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
        df_existing = pd.read_csv(csv_filename)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    # timestamp列をdatetime型に変換・整列
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values("timestamp", inplace=True)
    df_all.to_csv(csv_filename, index=False)
    print(f"✅ Data appended to {csv_filename}")

    # --- 銘柄ごとにPNG作成 ---
    colors = {
        "Gold": "gold",
        "Silver": "gray",
        "Platinum": "purple",
        "Palladium": "brown"
    }

    for name in tickers.values():
        df_sub = df_all[df_all["name"] == name]
        if df_sub.empty:
            print(f"⚠️ No data to plot for {name}")
            continue

        png_filename = f"{[k for k, v in tickers.items() if v == name][0].split('.')[0]}.png"

        plt.figure(figsize=(10, 8))

        # ETF価格とNAVを描画
        plt.plot(df_sub["timestamp"], df_sub["price"],
                 label=f"{name} ETF", color=colors[name], linestyle="-", marker="o")
        if df_sub["nav_jpy"].notna().any():
            plt.plot(df_sub["timestamp"], df_sub["nav_jpy"],
                     label=f"{name} NAV", color=colors[name], linestyle="--", marker="x")

        # 乖離率を第2軸で表示
        ax2 = plt.gca().twinx()
        ax2.plot(df_sub["timestamp"], df_sub["deviation_pct"],
                 label="Deviation (%)", color="red", linestyle=":", marker=".")

        plt.title(f"{name} ETF vs NAV (JPY)")
        plt.xlabel("Time (JST)")
        plt.ylabel("Price / NAV (JPY)")
        ax2.set_ylabel("Deviation (%)")

        plt.xticks(rotation=45, ha="right")

        # 凡例
        h1, l1 = plt.gca().get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(h1 + h2, l1 + l2, loc="best")

        plt.tight_layout()
        plt.savefig(png_filename)
        plt.close()
        print(f"✅ Chart updated: {png_filename}")

    # --- 最新乖離率の表示 ---
    print("\nLatest Deviation Rates:")
    for row in data:
        print(f"{row['name']} ({row['ticker']}) ETF%NAV: {row['deviation_pct']:.2f}%")

if __name__ == "__main__":
    main()
