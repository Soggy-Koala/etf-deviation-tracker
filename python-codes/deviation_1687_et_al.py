# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --- データ読み込み ---
    df = pd.read_csv("ETFdata.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- カラーマップ設定 ---
    colors = {
        "1687.T": "#DAA520",  # Agriculture - goldenrod,
        "1688.T": "#0000FF",  # Grains
        "1695.T": "#708090",  # Wheat
        "1696.T": "#8B4513",  #"Corn
        "1697.T": "#4daf4a",  #"Soybeans
    }

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))

    for ticker, color in colors.items():
        sub = df[df["ticker"] == ticker]
        plt.plot(sub["timestamp"], sub["deviation_pct"], label=ticker, color=color, linewidth=2)

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
