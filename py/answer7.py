import pandas as pd

# 讀取資料
df = pd.read_csv('./file/opendata114N010.csv')

# 刪除第一列的中文欄位說明
df = df.iloc[1:].copy()

# 將相關欄位轉換為數值型態 (若遇無法轉換的字串，例如 '…' 轉為 NaN)
cols_to_numeric = ['people_total', 'area', 'population_density']
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# =================================================================
# 1. 提取前三個字作為縣市名，計算「臺南市」的總人口數
# =================================================================
# 透過 site_id 前 3 個字元提取縣市名
df['city'] = df['site_id'].str[:3]

tainan_df = df[df['city'] == '臺南市']
tainan_total_pop = tainan_df['people_total'].sum()

print("第 1 題輸出：")
print(int(tainan_total_pop))
print("-" * 20)

# =================================================================
# 2. 人口密度大於 20,000 的行政區，由高到低排序取前三名
# =================================================================
high_density_df = df[df['population_density'] > 20000]
top3_density = high_density_df.sort_values(by='population_density', ascending=False).head(3)

print("第 2 題輸出：")
for _, row in top3_density.iterrows():
    # 輸出區域及數值 (依題目範例，此處將其轉為整數，或可視需求保留小數點)
    print(f"{row['site_id']} {int(row['population_density'])}")
print("-" * 20)

# =================================================================
# 3. 土地面積最小的前三個行政區 (排除無人區域)
# =================================================================
# 假設無人區域為總人口數等於 0 或為空值
inhabited_df = df[df['people_total'] > 0]
top3_smallest_area = inhabited_df.nsmallest(3, 'area')

print("第 3 題輸出：")
for _, row in top3_smallest_area.iterrows():
    print(f"{row['site_id']} {row['area']}")