# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- 監視対象ETF（米国ゴールド）---
etfs = {
    "GLD": "SPDR Gold Shares",
    "IAU": "iShares Gold Trust"
}

log_path = "gold_etf_us_deviation_log.csv"
all_rows = []

for ticker, name in etfs.items():
    etf = yf.Ticker(ticker)
    price = etf.history(period="1d")["Close"].iloc[-1]
    nav = etf.info.get("navPrice")  # yfinance info で取得可能
    deviation = (price - nav) / nav * 100 if nav else None

    all_rows.append({
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ticker": ticker,
        "name": name,
        "price": price,
        "nav": nav,
        "deviation(%)": deviation
    })

# CSV保存（既存ファイルがあれば追記）
df_new = pd.DataFrame(all_rows)
if os.path.exists(log_path):
    df_old = pd.read_csv(log_path)
    df_all = pd.concat([df_old, df_new], ignore_index=True)
else:
    df_all = df_new
df_all.to_csv(log_path, index=False)

# --- グラフ描画 ---
plt.figure(figsize=(10,5))
for ticker in etfs.keys():
    df_t = df_all[df_all["ticker"] == ticker]
    plt.plot(pd.to_datetime(df_t["datetime"]), df_t["deviation(%)"], marker="o", label=f"{ticker} US 乖離率(%)")

plt.title("米国GLD / IAU ETF NAV乖離率")
plt.xlabel("日時")
plt.ylabel("乖離率 (%)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("gold_etf_us_deviation.png")
plt.close()

print("✅ CSV・PNG 更新完了（US版）")
