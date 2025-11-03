# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def main():
    # --- ETF 1540.T ---
    goldetf_ticker = "1540.T"
    goldetf = yf.Ticker(goldetf_ticker)
    goldetf_price = goldetf.history(period="1d")["Close"].iloc[-1]
    goldinfo = goldetf.info
    goldnav = goldinfo.get('navPrice')
    goldnav_jpy = goldnav

    # --- 乖離率計算 ---
    gold_deviation = (goldetf_price - goldnav_jpy) / goldnav_jpy * 100

    # --- ログ保存 ---
    log_path = "gold_deviation_log.csv"
    new_row = pd.DataFrame({
        "date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "etf_price": [goldetf_price],
        "nav_price": [goldnav_jpy],
        "deviation(%)": [gold_deviation]
    })

    # CSV が存在する場合は読み込み、なければ新規作成
    if os.path.exists(log_path):
        df_old = pd.read_csv(log_path)
        df_all = pd.concat([df_old, new_row], ignore_index=True)
    else:
        df_all = new_row

    df_all.to_csv(log_path, index=False)

    # --- グラフ描画（価格と乖離率の2軸）---
    df_all["date"] = pd.to_datetime(df_all["date"])
    fig, ax1 = plt.subplots(figsize=(10,5))

    # 左軸：乖離率（%）
    ax1.set_xlabel("日付")
    ax1.set_ylabel("乖離率 (%)", color="blue")
    ax1.plot(df_all["date"], df_all["deviation(%)"], color="blue", marker="o", label="乖離率")
    ax1.tick_params(axis='y', labelcolor="blue")

    # 右軸：ETF価格
    ax2 = ax1.twinx()
    ax2.set_ylabel("ETF価格 (JPY)", color="orange")
    ax2.plot(df_all["date"], df_all["etf_price"], color="orange", marker="x", label="ETF価格")
    ax2.tick_params(axis='y', labelcolor="orange")

    plt.title("1540.T ETF価格とNAV乖離率の推移")
    plt.grid(True)
    fig.tight_layout()

    # PNG 保存（上書き）
    plt.savefig("gold_deviation.png")
    plt.close()

    print("===================")
    print("金1540")
    print(f"ETF価格: {goldetf_price:,.0f} JPY")
    print(f"NAV     : {goldnav_jpy:,.0f} JPY")
    print(f"乖離率  : {gold_deviation:.2f}%")
    print("-------------------")
    print("✅ CSV・PNG 更新完了")

if __name__ == "__main__":
    main()
