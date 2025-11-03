# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    # --- 取得時刻 ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- 各ETFのデータ取得 ---
    tickers = {
        "1672.T": "Gold",
        "1673.T": "Silver",
        "1674.T": "Platinum",
        "1675.T": "Palladium",
        "1676.T": "RoyalMetal"
    }

    results = []

    for tkr, name in tickers.items():
        t = yf.Ticker(tkr)
        price = t.history(period="1d")["Close"].iloc[-1]
        info = t.info
        nav = info.get('navPrice')
        if nav is None:
            continue
        fx = yf.Ticker("JPY=X")
        usd_jpy = fx.history(period="1d")["Close"].iloc[-1]
        nav_jpy = nav * usd_jpy
        deviation = (price - nav_jpy) / nav_jpy * 100
        results.append({
            "timestamp": timestamp,
            "ticker": tkr,
            "name": name,
            "price": price,
            "nav": nav_jpy,
            "deviation_pct": deviation
        })

    # --- DataFrame作成 ---
    df = pd.DataFrame(results)

    # --- ファイル保存 ---
    ts_short = datetime.now().strftime("%Y%m%d_%H%M")
    csv_filename = f"1672etal_data_{ts_short}.csv"
    png_filename = f"1672etal_chart_{ts_short}.png"
    df.to_csv(csv_filename, index=False)

    # --- プロット ---
    plt.figure(figsize=(10, 6))
    colors = {
        "1672.T": "gold",
        "1673.T": "silver",
        "1674.T": "plum",
        "1675.T": "gray",
        "1676.T": "orange"
    }

    for tkr in df["ticker"].unique():
        sub = df[df["ticker"] == tkr]
        c = colors.get(tkr, None)
        plt.plot(sub["timestamp"], sub["price"], label=f"{tkr} ETF", color=c, linestyle="-")
        plt.plot(sub["timestamp"], sub["nav"], label=f"{tkr} NAV", color=c, linestyle="--")

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Time (JST)")
    plt.ylabel("Price (JPY)")
    plt.title("ETF vs NAV (1672 et al)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_filename)

    print(f"Saved: {csv_filename}, {png_filename}")
    print(df[["ticker", "deviation_pct"]])

if __name__ == "__main__":
    main()
