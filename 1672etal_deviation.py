import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# データ保存
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
csv_filename = f"1672etal_data_{timestamp}.csv"
png_filename = f"1672etal_chart_{timestamp}.png"
df.to_csv(csv_filename, index=False)

# ======== 時系列プロット =========
df_sorted = df.sort_values(by="timestamp")  # timestamp で時系列ソート
plt.figure(figsize=(10, 6))

# 左軸：価格とNAV
plt.plot(df_sorted["timestamp"], df_sorted["price"], label="Market Price", marker="o")
plt.plot(df_sorted["timestamp"], df_sorted["nav"], label="NAV", marker="o")

# 右軸：乖離率（%）
ax2 = plt.gca().twinx()
ax2.plot(df_sorted["timestamp"], df_sorted["deviation_pct"], label="Deviation (%)", color="tab:red", linestyle="--", marker="x")

# 軸ラベルと凡例など
plt.gca().set_xlabel("Time (JST)")
plt.gca().set_ylabel("Price / NAV")
ax2.set_ylabel("Deviation (%)")
plt.title("1672 et al. Price vs NAV Deviation Over Time")
plt.xticks(rotation=45, ha="right")

# 凡例を統合
lines, labels = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines + lines2, labels + labels2, loc="best")

plt.tight_layout()
plt.savefig(png_filename)
print(f"Saved chart as {png_filename}")
