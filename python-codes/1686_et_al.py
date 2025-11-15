# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_single(df, target_name, output_filename):
    """1銘柄分をプロットしてPNGに保存"""
    df_sub = df[df["name"] == target_name]
    if df_sub.empty:
        print(f"⚠ データが見つかりません: {target_name}")
        return

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_price = "blue"
    color_deviation = "gray"

    # 左軸：ETFとNAV
    ax1.set_xlabel("Time (JST)")
    ax1.set_ylabel("Price (JPY)", color=color_price)
    ax1.plot(df_sub["timestamp"], df_sub["price"], label="ETF", color=color_price, linestyle="-", marker=".")
    if df_sub["nav_jpy"].notna().any():
        ax1.plot(df_sub["timestamp"], df_sub["nav_jpy"], label="NAV", color=color_price, linestyle="--", marker=".")
    ax1.tick_params(axis="y", labelcolor=color_price)

    # 右軸：乖離率
    ax2 = ax1.twinx()
    ax2.set_ylabel("Deviation (%)", color=color_deviation)
    ax2.plot(df_sub["timestamp"], df_sub["deviation_pct"], label="Deviation", color=color_deviation, linestyle=":", marker=".")
    ax2.tick_params(axis="y", labelcolor=color_deviation)

    # 凡例と体裁
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.title(f"ETF vs NAV and Deviation ({target_name})")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()

    plt.savefig(output_filename)
    plt.close()
    print(f"✅ Chart generated: {output_filename}")

def main():
    csv_filename = "ETFdata.csv"

    # --- CSVファイル確認 ---
    if not os.path.exists(csv_filename):
        print(f"❌ CSVファイルが見つかりません: {csv_filename}")
        return

    # --- CSV読み込み ---
    df = pd.read_csv(csv_filename)

    required_cols = {"timestamp", "ticker", "name", "price", "nav_jpy", "deviation_pct"}
    if not required_cols.issubset(df.columns):
        print("❌ CSVに必要な列がありません。")
        print(" 必須列:", required_cols)
        print(" 含まれている列:", df.columns.tolist())
        return

    # timestamp を datetime に変換してソート
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df.sort_values("timestamp", inplace=True)

    # --- 対象銘柄 ---
    tickers_1686 = {
        "1685.T": "Energy",
        "1689.T": "Natural Gas",
        "1690.T": "WTI Crude Oil",
        "1691.T": "Gasoline"
    }

    # --- 各銘柄ごとにPNG生成 ---
    for ticker, name in tickers.items():
        png_filename = f"{ticker.replace('.T', '')}.png"
        plot_single(df, name, png_filename)

if __name__ == "__main__":
    main()
