# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# ETF グループ定義（ここだけ編集すればOK）
# ==================================================
ETF_GROUPS = {
    "1672": {
        "title": "ETF Deviation (1672 et al)",
        "output": "deviation_1672_et_al.png",
        "tickers": {
            "1672.T": ("Gold", "#DAA520"),
            "1673.T": ("Silver", "#0000FF"),
            "1674.T": ("Platinum", "#708090"),
            "1675.T": ("Palladium", "#8B4513"),
            "1676.T": ("Noble Metal", "#800080"),
        },
    },
    "1685": {
        "title": "ETF Deviation (1685 et al)",
        "output": "deviation_1685_et_al.png",
        "tickers": {
            "1685.T": ("Energy", "#DAA520"),
            "1689.T": ("Natural Gas", "#0000FF"),
            "1690.T": ("WTI Crude Oil", "#708090"),
            "1691.T": ("Gasoline", "#8B4513"),
        },
    },
    "1686": {
        "title": "ETF Deviation (1686 et al)",
        "output": "deviation_1686_et_al.png",
        "tickers": {
            "1686.T": ("Ind. Metals", "#DAA520"), # goldenrod
            "1692.T": ("Alminum", "#0000FF"), # blue
            "1693.T": ("Copper", "#708090"), # slate gray
            "1694.T": ("Nickel", "#8B4513"), # saddle brown
        },
    },
    "1687": {
        "title": "ETF Deviation (1687 et al)",
        "output": "deviation_1687_et_al.png",
        "tickers": {
            "1687.T": ("Agriculture", "#DAA520"), # goldenrod
            "1688.T": ("Grains", "#0000FF"), # blue
            "1695.T": ("Wheat", "#708090"), # slate gray
            "1696.T": ("Corn", "#8B4513"), # saddle brown
            "1697.T": ("Soybeans", "#4daf4a"), # 
        },
    },
    "1540": {
        "title": "ETF Deviation (1540 et al)",
        "output": "deviation_1540_et_al.png",
        "tickers": {
            "1540.T": ("Gold", "#DAA520"), # goldenrod
            "1542.T": ("Silver", "#0000FF"), # blue
            "1541.T": ("Platinum", "#708090"), # slate gray
            "1543.T": ("Palladium", "#8B4513"), # saddle brown
        },
    },
}

# ==================================================
def draw_group(df, group):
    plt.figure(figsize=(10, 6))

    for ticker, (name, color) in group["tickers"].items():
        sub = df[df["ticker"] == ticker]
        if sub.empty:
            continue

        plt.plot(
            sub["timestamp"],
            sub["deviation_pct"],
            label=f"{ticker[:4]} {name}",
            color=color,
            linewidth=2,
        )

    plt.title(group["title"], fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Deviation (%)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Ticker")
    plt.tight_layout()

# ==================================================
def main():
    # --- データ読み込み（1回だけ） ---
    df = pd.read_csv("ETFdata.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # os.makedirs("png", exist_ok=True)

    # --- 全グループを順番に描画 ---
    for key, group in ETF_GROUPS.items():
        draw_group(df, group)

        #output_path = os.path.join("png", group["output"])
        output_path = os.path.join("", group["output"])
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"generated: {output_path}")

# ==================================================
if __name__ == "__main__":
    main()
