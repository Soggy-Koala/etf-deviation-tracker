# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --- データ読み込み ---
    df = pd.read_csv("ETFdata.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- カラーマップ設定 ---
    colors = {
        "1685.T": "#DAA520",  # Energy - goldenrod
        "1689.T": "#0000FF",  # Natural Gas - blue
        "1690.T": "#708090",  # WTI Crude Oil - slate gray
        "1691.T": "#8B4513",  # Gasoline - saddle brown
    }
    names = {
        "1685.T": "Energy",
        "1689.T": "Natural Gas",
        "1690.T": "WTI Crude Oil",
        "1691.T": "Gasoline"
    }

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))

    for ticker, color in colors.items():
        sub = df[df["ticker"] == ticker]
        plt.plot(sub["timestamp"], sub["deviation_pct"], label=ticker[0:4]+" "+names[ticker], color=color, linewidth=2)

    plt.title("ETF Deviation (1685 et al)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Deviation (%)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Ticker")
    plt.tight_layout()

    # --- 保存 ---
    plt.savefig("deviation_1685_et_al.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
