import pandas as pd

# 讀取資料
df = pd.read_csv('./file/NPA_TD1.csv')

# 刪除第一列的中文欄位說明
df = df.iloc[1:].copy()

# =================================================================
# 1. 全台各縣市中，測速照相點最多與最少的分別是哪個縣市及其數量？
# =================================================================
# 篩選名稱結尾是「縣」或「市」的資料，排除國道路線
cities_df = df[df['CityName'].str.endswith(('縣', '市'))].copy()
city_counts = cities_df['CityName'].value_counts()

max_city, max_cnt = city_counts.index[0], city_counts.iloc[0]
min_city, min_cnt = city_counts.index[-1], city_counts.iloc[-1]

print("第 1 題輸出：")
print(f"{max_city} {max_cnt}")
print(f"{min_city} {min_cnt}")
print("-" * 20)

# =================================================================
# 2. 哪些縣市擁有限速 100 的測速照相點？降冪排序
# =================================================================
# 將速限轉換為數值型態
cities_df['limit'] = pd.to_numeric(cities_df['limit'], errors='coerce')

# 篩選限速 100 的測速點
limit_100_cities = cities_df[cities_df['limit'] == 100]
limit_100_counts = limit_100_cities['CityName'].value_counts()

print("第 2 題輸出：")
for county, count in limit_100_counts.items():
    print(f"{county} {count}")
print("-" * 20)

# =================================================================
# 3. 國道公路警察局管轄內，數量最多的前三條路線
# =================================================================
# 篩選管轄警局為「國道公路警察局」的資料
highway_df = df[df['DeptNm'] == '國道公路警察局'].copy()

# 由於在國道警察局管轄下，其路線名稱是存在 'CityName' 欄位中
route_counts = highway_df['CityName'].value_counts().nlargest(3)

print("第 3 題輸出：")
for route, count in route_counts.items():
    print(f"{route} {count}")