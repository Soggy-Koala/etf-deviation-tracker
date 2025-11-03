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
    nav = etf.info.get("navPrice")
    deviation = (price - nav) / nav * 100 if nav else None

    all_rows.append({
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ticker": ticker,
        "name": name,
        "price": price,
        "nav": nav,
        "deviation(%)": deviation
    })

# CSV保存（既存ファイルに追記）
df_new = pd.DataFrame(all_rows)
if os.path.exists(log_path):
    df_old = pd.read_csv(log_path)
    df_all = pd.concat([df_old, df_new], ignore_index=True)
else:
    df_all = df_new
df_all.to_csv(log_path, index=False)

# --- 2軸グラフ描画 ---
plt.figure(figsize=(12,5))
ax1 = plt.gca()  # 左軸: 乖離率
ax2 = ax1.twinx()  # 右軸: ETF価格

for ticker in etfs.keys():
    df_t = df_all[df_all["ticker"] == ticker]
    times = pd.to_datetime(df_t["datetime"])
    # 左軸: 乖離率
    ax1.plot(times, df_t["deviation(%)"], marker="o", label=f"{ticker} US 乖離率(%)")
    # 右軸: 価格
    ax2.plot(times, df_t["price"], marker="x", linestyle="--", label=f"{ticker} 価格 (USD)")

# 軸ラベル
ax1.set_xlabel("日時")
ax1.set_ylabel("乖離率 (%)")
ax2.set_ylabel("価格 (USD)")

# タイトル
plt.title("米国GLD / IAU ETF NAV乖離率と価格")

# 凡例の整理（両軸）
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

ax1.grid(True)
plt.tight_layout()
plt.savefig("gold_etf_us_deviation.png")
plt.close()

print("✅ CSV・PNG 更新完了（価格付きグラフ）")
