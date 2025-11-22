# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --- データ読み込み ---
    df = pd.read_csv("ETFdata.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- カラーマップ設定 ---
    colors = {
        "1686.T":"#DAA520",  # Industrial Metals - goldenrod,
        "1692.T":"#0000FF",  # Aluminum - blue,
        "1693.T":"#708090",  # Copper - slate gray,
        "1694.T":"#8B4513",  # Nickel - saddle brown
    }
    names = {
        "1686.T":"Ind.Metals",
        "1692.T":"Aluminum", 
        "1693.T":"Copper", 
        "1694.T":"Nickel"
  }

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))

    for ticker, color in colors.items():
        sub = df[df["ticker"] == ticker]
        plt.plot(sub["timestamp"], sub["deviation_pct"], label=ticker[0:4]+" "+names[ticker], color=color, linewidth=2)

    plt.title("ETF Deviation (1686 et al)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Deviation (%)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Ticker")
    plt.tight_layout()

    # --- 保存 ---
    plt.savefig("deviation_1686_et_al.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
