import os
import pandas as pd
from datetime import datetime

log_path = "gold_deviation_log.csv"

# 新しいデータ
new_row = pd.DataFrame({
    "date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
    "etf_price": [goldetf_price],
    "nav_price": [goldnav_jpy],
    "deviation(%)": [gold_deviation]
})

# CSV が存在する場合だけ読み込む
if os.path.exists(log_path):
    df_old = pd.read_csv(log_path)
    df_all = pd.concat([df_old, new_row], ignore_index=True)
else:
    df_all = new_row

# CSV 保存
df_all.to_csv(log_path, index=False)

# --- グラフ描画（価格と乖離率の2軸）---
df_all["date"] = pd.to_datetime(df_all["date"])
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

plt.title("1540.T ETF価格とNAV乖離率の推移")
plt.grid(True)
fig.tight_layout()

# ✅ PNG 保存
plt.savefig("gold_deviation.png")
plt.close()

