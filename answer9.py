import pandas as pd

# 讀取並合併所有 CSV 檔案
files = [
    './file/20250930-DailyImmigPort.csv', './file/20251031-DailyImmigPort.csv', 
    './file/20251130-DailyImmigPort.csv', './file/20251231-DailyImmigPort.csv',
    './file/20260131-DailyImmigPort.csv', './file/20260228-DailyImmigPort.csv', 
    './file/20260331-DailyImmigPort.csv'
]
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs, ignore_index=True)

# 日期轉為 datetime 格式，其他需運算的欄位轉為數值型態
df['日期'] = pd.to_datetime(df['日期'].astype(str), format='%Y%m%d')
numeric_cols = df.columns.drop('日期')
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

# =========================================================
# ** 解決 Performance Warning 的核心優化 **
# 將所有要新增的輔助欄位先放在一個字典 (dict) 中，再一次性 concat
# =========================================================
new_cols = {}

# 建立輔助欄位以利快速篩選
new_cols['YM'] = df['日期'].dt.strftime('%Y-%m')  # 年-月
new_cols['Month'] = df['日期'].dt.month           # 月份數值
new_cols['DayOfWeek'] = df['日期'].dt.dayofweek   # 星期 (5=週六, 6=週日)

# 準備第 18 題需要的欄位
in_cols = [c for c in df.columns if '入境查驗' in c]
out_cols = [c for c in df.columns if '出境查驗' in c]
new_cols['全台總入境'] = df[in_cols].sum(axis=1)
new_cols['全台總出境'] = df[out_cols].sum(axis=1)
new_cols['不平衡度'] = new_cols['全台總入境'] - new_cols['全台總出境']

# 準備第 19 題需要的欄位
port_cols = [c for c in df.columns if c.endswith('港小計')]
air_cols = [c for c in df.columns if c.endswith('機場小計')]
new_cols['港口類'] = df[port_cols].sum(axis=1)
new_cols['機場類'] = df[air_cols].sum(axis=1)

# 一次性合併，避免 fragmented warning
new_df_part = pd.DataFrame(new_cols)
df = pd.concat([df, new_df_part], axis=1)

# 產生一個連續記憶體的全新 DataFrame，確保最佳效能
df = df.copy()
# =========================================================

# (以下列印與計算邏輯完全維持不變)

# =========================================================
print("1.")
sum_09 = df[df['YM'] == '2025-09']['入出境總人數_小計'].sum()
sum_10 = df[df['YM'] == '2025-10']['入出境總人數_小計'].sum()
print(int(sum_09),int(sum_10))

# =========================================================
print("\n2.")
sum_12 = df[df['YM'] == '2025-12']['桃園一_二期合計'].sum()
sum_01 = df[df['YM'] == '2026-01']['桃園一_二期合計'].sum()
print(int(sum_01 - sum_12))

# =========================================================
print("\n3.")
df_2_3 = df[df['YM'].isin(['2026-02', '2026-03'])]
sum_songshan = df_2_3['松山機場小計'].sum()
max_idx = df_2_3['松山機場小計'].idxmax()
max_date = df_2_3.loc[max_idx, '日期']
print(int(sum_songshan))
print(f"{max_date.month}/{max_date.day}")

# =========================================================
print("\n4.")
sum_k_09 = df[df['YM'] == '2025-09']['高雄機場小計'].sum()
sum_k_10 = df[df['YM'] == '2025-10']['高雄機場小計'].sum()
sum_k_11 = df[df['YM'] == '2025-11']['高雄機場小計'].sum()
mom_10 = (sum_k_10 - sum_k_09) / sum_k_09 * 100
mom_11 = (sum_k_11 - sum_k_10) / sum_k_10 * 100
print(int(sum_k_09))
print(f"{int(sum_k_10)} {mom_10:.2f}%")
print(f"{int(sum_k_11)} {mom_11:.2f}%")

# =========================================================
print("\n5.")
df_12 = df[df['YM'] == '2025-12']
df_01 = df[df['YM'] == '2026-01']
max_12_idx = df_12['金門港_水頭小計'].idxmax()
max_01_idx = df_01['金門港_水頭小計'].idxmax()
date_12 = df_12.loc[max_12_idx, '日期']
date_01 = df_01.loc[max_01_idx, '日期']
print(f"{date_12.month}/{date_12.day} {int(df_12.loc[max_12_idx, '金門港_水頭小計'])}")
print(f"{date_01.month}/{date_01.day} {int(df_01.loc[max_01_idx, '金門港_水頭小計'])}")

# =========================================================
print("\n6.")
max_p = 0
max_m = None
# 計算 9至12月中，最高佔比的月份
for m in [9, 10, 11, 12]:
    temp = df[(df['YM'].str.startswith('2025')) & (df['Month'] == m)]
    p = temp['桃園一期入境查驗'].sum() / temp['桃園一期小計'].sum()
    if p > max_p:
        max_p = p
        max_m = m
print(f"{max_m}月")

# =========================================================
print("\n7.")
df_q4 = df[df['YM'].isin(['2025-10', '2025-11', '2025-12'])]
sum_tc = df_q4['台中機場小計'].sum()
avg_tc = df_q4['台中機場小計'].mean()
print(f"{int(sum_tc)} {avg_tc:.2f}")

# =========================================================
print("\n8.")
matsu_max_01 = df_01['馬祖小計'].max()
matsu_02 = df[df['YM'] == '2026-02']
over_days = matsu_02[matsu_02['馬祖小計'] > matsu_max_01]
if not over_days.empty:
    for _, row in over_days.iterrows():
        print(f"{row['日期'].month}/{row['日期'].day} {int(row['馬祖小計'])}")
else:
    print("未超過")

# =========================================================
print("\n9.")
df_9_12 = df[df['YM'].isin(['2025-09', '2025-10', '2025-11', '2025-12'])]
avg_9_12 = df_9_12.groupby('Month')['入出境總人數_小計'].mean().sort_values(ascending=False)
for idx, val in avg_9_12.items():
    print(f"{idx}月 {val:.2f}")

# =========================================================
print("\n10.")
# DayOfWeek: 5為週六, 6為週日
df_wknd = df[(df['YM'].isin(['2025-09', '2025-10'])) & (df['DayOfWeek'] >= 5)]
sum_kl_wknd = df_wknd['基隆港小計'].sum()
print(int(sum_kl_wknd))

# =========================================================
print("\n11.")
avg_1 = df[df['YM'] == '2026-01']['高雄港小計'].mean()
avg_2 = df[df['YM'] == '2026-02']['高雄港小計'].mean()
avg_3 = df[df['YM'] == '2026-03']['高雄港小計'].mean()

avgs = {1: avg_1, 2: avg_2, 3: avg_3}
best_month = max(avgs, key=avgs.get)

print(f"{best_month}月")
for m, v in avgs.items():
    print(f"{m}月 {v:.2f}")

# =========================================================
print("\n12.")
std_11 = df[df['YM'] == '2025-11']['桃園二期小計'].std()
std_12 = df[df['YM'] == '2025-12']['桃園二期小計'].std()
print(f"11月 {std_11:.2f}")
print(f"12月 {std_12:.2f}")

# =========================================================
print("\n13.")
c_1 = len(df[(df['YM'] == '2026-01') & (df['入出境總人數_小計'] > 150000)])
c_2 = len(df[(df['YM'] == '2026-02') & (df['入出境總人數_小計'] > 150000)])
print(f"1月 {c_1}")
print(f"2月 {c_2}")

# =========================================================
print("\n14.")
sum_tn = df[df['YM'].isin(['2025-09', '2025-10', '2025-11'])]['台南機場小計'].sum()
print(int(sum_tn))

# =========================================================
print("\n15.")
hl_09 = df[df['YM'] == '2025-09']['花蓮機場小計'].sum()
hl_03 = df[df['YM'] == '2026-03']['花蓮機場小計'].sum()
print(int(hl_03 - hl_09))

# =========================================================
print("\n16.")
overall_mean = df['入出境總人數_小計'].mean()
threshold = overall_mean * 1.2
over_thr_df = df[df['入出境總人數_小計'] > threshold]

for _, row in over_thr_df.iterrows():
    print(f"{row['日期'].month}/{row['日期'].day} {int(row['入出境總人數_小計'])}")

# =========================================================
print("\n17.")
ports = ['松山機場小計', '高雄機場小計', '桃園一期小計', '桃園二期小計']
monthly_sums = df.groupby('YM')[ports].sum()

cvs = {}
for p in ports:
    cv = monthly_sums[p].std() / monthly_sums[p].mean()
    cvs[p] = cv

winner = min(cvs, key=cvs.get)
print(f"{winner}")

# =========================================================
print("\n18.")
max_diff_idx = df['不平衡度'].abs().idxmax()
val = df.loc[max_diff_idx, '不平衡度']
direction = "入境" if val > 0 else "出境"
target_date = df.loc[max_diff_idx, '日期']

print(f"{target_date.month}/{target_date.day} {direction} {int(abs(val))}")

# =========================================================
print("\n19.")
port_09 = df[df['YM'] == '2025-09']['港口類'].sum()
port_03 = df[df['YM'] == '2026-03']['港口類'].sum()
air_09 = df[df['YM'] == '2025-09']['機場類'].sum()
air_03 = df[df['YM'] == '2026-03']['機場類'].sum()

print(f"{((port_03 - port_09) / port_09) * 100:.2f}% {((air_03 - air_09) / air_09) * 100:.2f}%")

# =========================================================
print("\n20.")
top3 = df.nlargest(3, '入出境總人數_小計')

for _, row in top3.iterrows():
    pct = (row['桃園一_二期合計'] / row['入出境總人數_小計']) * 100
    print(f"{row['日期'].month}/{row['日期'].day} {pct:.2f}%")