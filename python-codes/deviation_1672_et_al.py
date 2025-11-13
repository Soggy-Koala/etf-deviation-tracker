# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # === CSV 読み込み ===
    csv_filename = "ETFdata.csv"
    df = pd.read_csv(csv_filename)

    # timestampをdatetimeに変換
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 対象ティッカー
    tickers = ["1672.T", "1673.T", "1674.T", "1675.T", "1676.T"]

    # === プロット設定 ===
    plt.figure(figsize=(12, 6))

    for ticker in tickers:
        df_t = df[df["ticker"] == ticker]
        if df_t.empty:
            continue
        label = df_t["name"].iloc[-1] if "name" in df_t.columns else ticker
        plt.plot(df_t["timestamp"], df_t["deviation_pct"], label=label)

    # === グラフデザイン ===
    plt.title("ETF 乖離率の推移 (1672–1676)", fontsize=14)
    plt.xlabel("日時", fontsize=12)
    plt.ylabel("乖離率 (%)", fontsize=12)
    plt.legend(title="銘柄", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # === 保存 ===
    output_file = "ETF_deviation_plot.png"
    plt.savefig(output_file, dpi=300)
    print(f"✅ グラフを保存しました: {output_file}")

if __name__ == "__main__":
    main()
