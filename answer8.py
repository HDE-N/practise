import pandas as pd

# 讀取 CSV 資料檔
df = pd.read_csv('./file/20250930-DailyImmigPort.csv')

# 確保日期為字串，其餘欄位轉為數值型態以利運算
df['日期'] = df['日期'].astype(str)
for col in df.columns:
    if col != '日期':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# =================================================================
# 1. 找出日期為「20250927」的入出境紀錄
# =================================================================
q1_data = df[df['日期'] == '20250927']
q1_total = int(q1_data['入出境總人數_小計'].values[0])
q1_taoyuan = int(q1_data['桃園一_二期合計'].values[0])

print("第 1 題輸出：")
print(f"{q1_total} {q1_taoyuan}")
print("-" * 20)

# =================================================================
# 2. 「入出境總人數_小計」最高的天數與數值
# =================================================================
max_idx = df['入出境總人數_小計'].idxmax()
max_total = int(df.loc[max_idx, '入出境總人數_小計'])
raw_date = df.loc[max_idx, '日期']  # 取得原始字串，例如 '20250928'

# 將 YYYYMMDD 格式透過字串切片並轉為整數以去除前導零，組合為 m/d
month = int(raw_date[4:6])
day = int(raw_date[6:8])
formatted_date = f"{month}/{day}"

print("第 2 題輸出：")
print(f"{max_total} {formatted_date}")
print("-" * 20)

# =================================================================
# 3. 「松山機場入境查驗」的累計總人數
# =================================================================
songshan_in_sum = int(df['松山機場入境查驗'].sum())

print("第 3 題輸出：")
print(songshan_in_sum)
print("-" * 20)

# =================================================================
# 4. 「入出境總人數_小計」大於平均值的天數
# =================================================================
mean_val = df['入出境總人數_小計'].mean()
count_greater = (df['入出境總人數_小計'] > mean_val).sum()

print("第 4 題輸出：")
print(count_greater)