# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def main():
    tickers = {"1672.T": "Gold"}
    usd_jpy = yf.Ticker("JPY=X").history(period="1d")["Close"].iloc[-1]

    data = []
    for ticker, name in tickers.items():
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if hist.empty:
            print(f"⚠️ {ticker} に価格データがありません。")
            continue

        price = hist["Close"].iloc[-1]
        info = t.info
        nav = info.get("navPrice") or info.get("previousClose")

        print(f"{name}: price={price}, nav={nav}")  # デバッグ出力

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

    csv_filename = "1672withDeviation.csv"
    png_filename = "1672withDeviation.png"

    # --- CSV追記 ---
    df_new = pd.DataFrame(data)
    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values("timestamp", inplace=True)
    df_all.to_csv(csv_filename, index=False)

    # --- プロット ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    color = "gold"

    for name in tickers.values():
        df_sub = df_all[df_all["name"] == name]
        if df_sub.empty:
            continue

        # 上段：価格・NAV
        ax1.plot(df_sub["timestamp"], df_sub["price"], label=f"{name} ETF", color=color, marker="o")
        if df_sub["nav_jpy"].notna().any():
            ax1.plot(df_sub["timestamp"], df_sub["nav_jpy"], label=f"{name} NAV", color=color, linestyle="--", marker="x")

        # 下段：乖離率
        if df_sub["deviation_pct"].notna().any():
            ax2.plot(df_sub["timestamp"], df_sub["deviation_pct"], label=f"{name} Deviation (%)", color=color, marker="o")

    # --- 軸・凡例など ---
    ax1.set_ylabel("Price / NAV (JPY)")
    ax1.set_title("ETF vs NAV (1672)")
    ax1.legend()

    ax2.set_xlabel("Time (JST)")
    ax2.set_ylabel("Deviation (%)")
    ax2.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax2.legend()

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(png_filename)
    plt.close()

    # --- 最新乖離率をコンソール表示 ---
    for row in data:
        if row['deviation_pct'] is not None:
            print(f"{row['name']} ({row['ticker']}): 乖離率 = {row['deviation_pct']:.2f}%")
        else:
            print(f"{row['name']} ({row['ticker']}): NAV 取得不可")

    print(f"✅ Data appended to {csv_filename}")
    print(f"✅ Chart updated: {png_filename}")

if __name__ == "__main__":
    main()
