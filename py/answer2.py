import pandas as pd

# 讀取資料
df = pd.read_csv('./file/aqx_p_432.csv')

# 資料清理：將 aqi 與 pm2.5 轉換為數值，若遇非數值（如空字串或 'ND'）則轉為 NaN
df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
df['pm2.5'] = pd.to_numeric(df['pm2.5'], errors='coerce')

# =================================================================
# 1. 臺北市 AQI 最高的前三名測站
# =================================================================
print("第 1 題輸出：")
taipei_df = df[df['county'] == '臺北市'].dropna(subset=['aqi'])
top3_taipei = taipei_df.sort_values(by='aqi', ascending=False).head(3)
for _, row in top3_taipei.iterrows():
    print(f"{row['sitename']} {int(row['aqi'])}")
print("-" * 20)

# =================================================================
# 2. PM2.5 平均濃度最高的前三個縣市
# =================================================================
print("第 2 題輸出：")
pm25_mean = df.groupby('county')['pm2.5'].mean().dropna()
top3_counties = pm25_mean.sort_values(ascending=False).head(3)
for county, val in top3_counties.items():
    # 取到小數點後兩位
    print(f"{county} {val:.2f}")
print("-" * 20)

# =================================================================
# 3. 狀態為「良好」與「普通」的測站數量，及「普通」狀態中 AQI 最高的測站
# =================================================================
print("第 3 題輸出：")
good_count = (df['status'] == '良好').sum()
moderate_count = (df['status'] == '普通').sum()

print(f"{good_count} {moderate_count}")

# 找出「普通」狀態中 AQI 最高的測站
moderate_df = df[df['status'] == '普通'].dropna(subset=['aqi'])
if not moderate_df.empty:
    max_moderate = moderate_df.loc[moderate_df['aqi'].idxmax()]
    print(f"{max_moderate['sitename']} {int(max_moderate['aqi'])}")