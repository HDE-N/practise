import pandas as pd

# 讀取 JSON 檔案
df = pd.read_json('./file/每日各站進出站人數-2026.json')

# 資料型態轉換
# 確保進出站人數為數值格式，以便後續進行加總與比較
df['gateInComingCnt'] = pd.to_numeric(df['gateInComingCnt'])
df['gateOutGoingCnt'] = pd.to_numeric(df['gateOutGoingCnt'])

# 確保車站代碼為字串型態，並補齊前導零（假設車站代碼均為 4 碼）
df['staCode'] = df['staCode'].astype(str).str.zfill(4)
# 確保日期為字串型態
df['trnOpDate'] = df['trnOpDate'].astype(str)


# =================================================================
# 1. 日期為「20260401」且車站代碼為「0900」的進站與出站人數
# =================================================================
print("第 1 題輸出：")
q1_data = df[(df['trnOpDate'] == '20260401') & (df['staCode'] == '0900')]
if not q1_data.empty:
    in_cnt = q1_data['gateInComingCnt'].values[0]
    out_cnt = q1_data['gateOutGoingCnt'].values[0]
    print(f"{in_cnt} {out_cnt}")
print("-" * 20)


# =================================================================
# 2. 車站代碼「0920」在整份資料期間的「總進站人數」
# =================================================================
print("第 2 題輸出：")
total_in_0920 = df[df['staCode'] == '0920']['gateInComingCnt'].sum()
print(total_in_0920)
print("-" * 20)


# =================================================================
# 3. 「進站人數」嚴格大於「出站人數」的資料總數
# =================================================================
print("第 3 題輸出：")
in_greater_out_cnt = len(df[df['gateInComingCnt'] > df['gateOutGoingCnt']])
print(in_greater_out_cnt)
print("-" * 20)


# =================================================================
# 4. 「20260101」，出站人數最高的前三名車站代碼及出站人數
# =================================================================
print("第 4 題輸出：")
ny_data = df[df['trnOpDate'] == '20260101']
# 依出站人數降冪排序並取前 3 名
top3_ny_out = ny_data.sort_values(by='gateOutGoingCnt', ascending=False).head(3)

for _, row in top3_ny_out.iterrows():
    print(f"{row['staCode']} {row['gateOutGoingCnt']}")