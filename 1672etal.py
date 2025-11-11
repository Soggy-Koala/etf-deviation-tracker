# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def main():
    tickers = {
        "1672.T": "Gold",
        "1673.T": "Silver",
        "1674.T": "Platinum",
        "1675.T": "Palladium",
    }

    usd_jpy = yf.Ticker("JPY=X").history(period="1d")["Close"].iloc[-1]

    # --- 新しいデータ取得 ---
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

    # --- CSV 蓄積 ---
    csv_filename = "1672etal.csv"
    df_new = pd.DataFrame(data)
    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values(["name", "timestamp"], inplace=True)
    df_all.to_csv(csv_filename, index=False)

    print(f"✅ Data appended to {csv_filename}")

    # --- グラフ作成 ---
    colors = {
        "Gold": "gold",
        "Silver": "gray",
        "Platinum": "purple",
        "Palladium": "brown",
    }

    for name in tickers.values():
        df_sub = df_all[df_all["name"] == name]
        if df_sub.empty:
            continue

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # --- 上段：価格/NAV ---
        ax1.plot(df_sub["timestamp"], df_sub["price"], color=colors[name], linestyle="-", label=f"{name} ETF")
        if df_sub["nav_jpy"].notna().any():
            ax1.plot(df_sub["timestamp"], df_sub["nav_jpy"], color=colors[name], linestyle="--", label=f"{name} NAV")

        ax1.set_xlabel("Time (JST)")
        ax1.set_ylabel("Price (JPY)")
        ax1.legend(loc="upper left")
        ax1.set_title(f"{name} ETF vs NAV ({df_sub['ticker'].iloc[0]})")

        # --- 下段：乖離率 ---
        ax2 = ax1.twinx()
        ax2.plot(df_sub["timestamp"], df_sub["deviation_pct"], color="black", linestyle=":", marker="o", label="Deviation (%)")
        ax2.set_ylabel("Deviation (%)")

        # 凡例・体裁
        fig.autofmt_xdate()
        plt.tight_layout()
        plt.savefig(f"{df_sub['ticker'].iloc[0].replace('.T','')}.png")
        plt.close()

        print(f"📈 Chart updated: {df_sub['ticker'].iloc[0].replace('.T','')}.png")

    # --- 最新の乖離率を表示 ---
    for row in data:
        print(f"{row['name']} ({row['ticker']}) ETF%NAV: {row['deviation_pct']:.2f}%")

if __name__ == "__main__":
    main()
