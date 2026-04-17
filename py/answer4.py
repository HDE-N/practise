import pandas as pd

# 讀取資料
df = pd.read_csv('./file/STOCK_DAY_ALL_20260401.csv')

# 確保計算欄位為數值型態（轉換無法轉換的字串為 NaN）
numeric_cols = ['最高價', '最低價', '成交筆數', '成交金額', '收盤價', '開盤價']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# =================================================================
# 1. 計算每檔股票的「當日價差」，找出當日價差最大的「前三名」股票
# =================================================================
df['當日價差'] = df['最高價'] - df['最低價']
top3_spread = df.nlargest(3, '當日價差')

print("第 1 題輸出：")
for _, row in top3_spread.iterrows():
    print(f"{row['證券名稱']} {row['當日價差']:.2f}")
print("-" * 20)

# =================================================================
# 2. 篩選「成交筆數」大於 10,000 筆，找出「成交金額」最高的一檔
# =================================================================
hot_stocks = df[df['成交筆數'] > 10000]

print("第 2 題輸出：")
if not hot_stocks.empty:
    highest_value_stock = hot_stocks.loc[hot_stocks['成交金額'].idxmax()]
    print(f"{highest_value_stock['證券名稱']} {int(highest_value_stock['成交金額'])}")
print("-" * 20)

# =================================================================
# 3. 找出所有「收盤價」大於「開盤價」的股票並計算數量
# =================================================================
up_stocks_count = (df['收盤價'] > df['開盤價']).sum()

print("第 3 題輸出：")
print(up_stocks_count)