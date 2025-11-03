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
