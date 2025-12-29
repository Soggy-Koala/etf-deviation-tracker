# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================================================
# グループ設定（銘柄だけをここに書く）
# ==================================================
GROUPS = {
    "1672": {
        "tickers": {
            "1672.T": "Gold",
            "1673.T": "Silver",
            "1674.T": "Platinum",
            "1675.T": "Palladium",
            "1676.T": "Noble Metal",
        }
    },
    "1685": {
        "tickers": {
            "1685.T": "Energy",
            "1689.T": "Natural Gas",
            "1690.T": "WTI Crude Oil",
            "1691.T": "Gasoline",
        }
    },
    # 1686 / 1687 / 1540 を同様に追加
}

# ==================================================
def plot_single(df, target_name, output_filename):
    """1銘柄分をプロットしてPNGに保存（1672方式の色分け）"""
    df_sub = df[df["name"] == target_name]
    if df_sub.empty:
        print(f"⚠ データが見つかりません: {target_name}")
        return

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # --- 色（1672_et_al.py 準拠） ---
    color_etf_price = "blue"
    color_nav_price = "orange"
    color_deviation = "gray"
    color_price = "black"

    # --- 左軸：ETF / NAV ---
    ax1.set_xlabel("Time (JST)")
    ax1.set_ylabel("Price (JPY)", color=color_price)

    ax1.plot(
        df_sub["timestamp"], df_sub["price"],
        label="ETF",
        color=color_etf_price,
        linestyle="-",
        marker="."
    )

    if df_sub["nav_jpy"].notna().any():
        ax1.plot(
            df_sub["timestamp"], df_sub["nav_jpy"],
            label="NAV",
            color=color_nav_price,
            linestyle="--",
            marker="."
        )

    ax1.tick_params(axis="y", labelcolor=color_price)

    # --- 右軸：乖離率 ---
    ax2 = ax1.twinx()
    ax2.set_ylabel("Deviation (%)", color=color_deviation)

    ax2.plot(
        df_sub["timestamp"], df_sub["deviation_pct"],
        label="Deviation",
        color=color_deviation,
        linestyle=":",
        marker="."
    )

    ax2.tick_params(axis="y", labelcolor=color_deviation)

    # --- 凡例・体裁 ---
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.title(f"ETF vs NAV and Deviation ({target_name})")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()

    plt.savefig(output_filename)
    plt.close()
    print(f"✅ Chart generated: {output_filename}")

# ==================================================
def main():
    csv_filename = "ETFdata.csv"

    if not os.path.exists(csv_filename):
        print(f"❌ CSVファイルが見つかりません: {csv_filename}")
        return

    df = pd.read_csv(csv_filename)

    required_cols = {"timestamp", "ticker", "name", "price", "nav_jpy", "deviation_pct"}
    if not required_cols.issubset(df.columns):
        print("❌ CSVに必要な列がありません。")
        print(" 必須列:", required_cols)
        print(" 含まれている列:", df.columns.tolist())
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df.sort_values("timestamp", inplace=True)

    os.makedirs("png", exist_ok=True)

    # --- 全グループ・全銘柄を一気に生成 ---
    for group in GROUPS.values():
        for ticker, name in group["tickers"].items():
            png_filename = f"png/{ticker.replace('.T', '')}.png"
            plot_single(df, name, png_filename)

# ==================================================
if __name__ == "__main__":
    main()
