# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    csv_filename = "ETFdata.csv"
    png_filename = "1672.png"
    target_name = "Gold"   # ← ETFdata.csv 内の "name" 列の値で指定

    # --- CSVファイル確認 ---
    if not os.path.exists(csv_filename):
        print(f"❌ CSVファイルが見つかりません: {csv_filename}")
        return

    # --- CSV読み込み ---
    df = pd.read_csv(csv_filename)

    if "timestamp" not in df.columns:
        print("❌ timestamp 列が見つかりません。")
        return

    # timestamp を datetime に変換してソート
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df.sort_values("timestamp", inplace=True)

    # --- 対象銘柄を抽出 ---
    df_sub = df[df["name"] == target_name]
    if df_sub.empty:
        print(f"⚠ データが見つかりません: {target_name}")
        return

    # --- グラフ描画 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_price = "blue"
    color_deviation = "black"

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

    # --- 保存 ---
    plt.savefig(png_filename)
    plt.close()

    print(f"✅ Chart generated: {png_filename}")

if __name__ == "__main__":
    main()
