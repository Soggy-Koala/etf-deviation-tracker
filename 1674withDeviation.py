# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def main():
    # --- 銘柄リスト ---
    tickers = {"1673.T": "Silver"}

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

    # --- ファイル設定 ---
    csv_filename = "1672withDeviation.csv"
    png_filename = "1673withDeviation.png"

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

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))
    color_price = "blue"
    color_deviation = "black"

    df_sub = df_all[df_all["name"] == "Silver"]

    if not df_sub.empty:
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 左軸（ETFとNAV）
        ax1.set_xlabel("Time (JST)")
        ax1.set_ylabel("Price (JPY)", color=color_price)
        ax1.plot(df_sub["timestamp"], df_sub["price"], label="ETF", color=color_price, linestyle="-", marker="o")
        if df_sub["nav_jpy"].notna().any():
            ax1.plot(df_sub["timestamp"], df_sub["nav_jpy"], label="NAV", color=color_price, linestyle="--", marker="x")
        ax1.tick_params(axis="y", labelcolor=color_price)

        # 右軸（乖離率）
        ax2 = ax1.twinx()
        ax2.set_ylabel("Deviation (%)", color=color_deviation)
        ax2.plot(df_sub["timestamp"], df_sub["deviation_pct"], label="Deviation", color=color_deviation, linestyle=":", marker="s")
        ax2.tick_params(axis="y", labelcolor=color_deviation)

        # 凡例
        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
        plt.title("ETF vs NAV and Deviation (1673)")
        fig.tight_layout()
        plt.xticks(rotation=45, ha="right")

        plt.savefig(png_filename)
        plt.close()

    print(f"✅ Data appended to {csv_filename}")
    print(f"✅ Chart updated: {png_filename}")

if __name__ == "__main__":
    main()
