# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --- データ読み込み ---
    df = pd.read_csv("ETFdata.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- カラーマップ設定 ---
    colors = {
        "1540.T": "#DAA520",  # Gold - goldenrod
        "1542.T": "#0000FF",  # Silver - dark gray
        "1541.T": "#708090",  # Platinum - slate gray
        "1543.T": "#8B4513"  # Palladium - saddle brown
    }
    names = {
        "1540.T": "Gold",
        "1542.T": "Silver",
        "1541.T": "Platinum",
        "1543.T": "Palladium"
    }

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))

    for ticker, color in colors.items():
        sub = df[df["ticker"] == ticker]
        plt.plot(sub["timestamp"], sub["deviation_pct"], label=ticker[0:4]+names[ticker], color=color, linewidth=2)

    plt.title("ETF Deviation (1540 et al)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Deviation (%)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Ticker")
    plt.tight_layout()

    # --- 保存 ---
    plt.savefig("deviation_1540_et_al.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
