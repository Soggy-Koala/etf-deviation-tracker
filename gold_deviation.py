import matplotlib.pyplot as plt
import pandas as pd

# CSV 読み込み（すでに df_all がある場合は不要）
df_all = pd.read_csv("gold_deviation_log.csv")

# 日付を datetime 型に変換
df_all["date"] = pd.to_datetime(df_all["date"])

# プロット
fig, ax1 = plt.subplots(figsize=(10,5))

# 左軸：乖離率（%）
ax1.set_xlabel("日付")
ax1.set_ylabel("乖離率 (%)", color="blue")
ax1.plot(df_all["date"], df_all["deviation(%)"], color="blue", marker="o", label="乖離率")
ax1.tick_params(axis='y', labelcolor="blue")

# 右軸：ETF価格
ax2 = ax1.twinx()
ax2.set_ylabel("ETF価格 (JPY)", color="orange")
ax2.plot(df_all["date"], df_all["etf_price"], color="orange", marker="x", label="ETF価格")
ax2.tick_params(axis='y', labelcolor="orange")

# タイトルとグリッド
plt.title("1540.T ETF価格とNAV乖離率の推移")
fig.tight_layout()
plt.grid(True)

# PNG 保存
plt.savefig("gold_deviation.png")
plt.close()
