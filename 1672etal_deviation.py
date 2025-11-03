# -*- coding: utf-8 -*-
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    # --- 現在時刻でファイル名を作成 ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv_filename = f"1672etal_data_{timestamp}.csv"
    png_filename = f"1672etal_chart_{timestamp}.png"

    # --- 各ETFの設定 ---
    tickers = {
        "金1672": "1672.T",
        "銀1673": "1673.T",
        "白金1674": "1674.T",
        "パラジウム1675": "1675.T",
        "貴金属1676": "1676.T",
    }

    # 色を統一（ETF実線 / NAV点線）
    colors = {
        "金1672": "gold",
        "銀1673": "silver",
        "白金1674": "gray",
        "パラジウム1675": "brown",
        "貴金属1676": "purple",
    }

    results = {}

    # --- 為替レート ---
    fx = yf.Ticker("JPY=X")
    usd_jpy = fx.history(period="1d")["Close"].iloc[-1]

    for name, ticker in tickers.items():
        etf = yf.Ticker(ticker)
        price = etf.history(period="1d")["Close"].iloc[-1]
        info = etf.info
        nav = info.get("navPrice")

        if nav is None:
            nav_jpy = None
            deviation = None
        else:
            nav_jpy = nav * usd_jpy
            deviation = (price - nav_jpy) / nav_jpy * 100

        results[name] = {
            "ETF価格": price,
            "NAV(JPY換算)": nav_jpy,
            "乖離率%": deviation
        }

    # --- 結果をCSV出力 ---
    import pandas as pd
    df = pd.DataFrame(results).T
    df.to_csv(csv_filename, encoding="utf-8-sig")
    print(f"✅ {csv_filename} を出力しました")

    # --- グラフ描画 ---
    plt.figure(figsize=(10, 6))
    for name in tickers.keys():
        c = colors[name]
        etf_price = results[name]["ETF価格"]
        nav_jpy = results[name]["NAV(JPY換算)"]
        if nav_jpy is not None:
            plt.plot([name], [etf_price], "o-", color=c, label=f"{name} ETF")
            plt.plot([name], [nav_jpy], "x--", color=c, label=f"{name} NAV")

    plt.title("ETFとNAVの比較（1672etal）")
    plt.ylabel("価格 [JPY]")
    plt.legend(fontsize=8, loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(png_filename, dpi=300)
    print(f"✅ {png_filename} を出力しました")

    # --- コンソール表示 ---
    print("\n===== 価格・乖離率 =====")
    for name, v in results.items():
        if v["乖離率%"] is not None:
            print(f"{name}: ETF={v['ETF価格']:.0f} JPY, NAV={v['NAV(JPY換算)']:.0f} JPY, 乖離={v['乖離率%']:.2f}%")
        else:
            print(f"{name}: ETF={v['ETF価格']:.0f} JPY, NAV=取得不可")

if __name__ == "__main__":
    main()
