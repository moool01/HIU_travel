import pandas as pd   
import json 
from haversine import haversine

file_path = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/관광지.json"

with open(file_path,'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df.head())
#info
df.info() #941개의 데이터(행), 15개의 열

#1. 결측치가 "", "정보 없음", "없음"과 같이 표현된 걸 확인, 결측치 처리 필요.
df.replace(['정보 없음', '',"", 'nan nan', '없음'], pd.NA, inplace=True)
# 'address' 열의 'nan' 제거
df['address'] = df['address'].str.replace('nan', '')
print(df.head())
df.info()

#2. 특수문자 제거나, 문자열 
#3.제주도 위도,경도 범위확인해보기 제주도 위도 경도는 
#위도:33.16~33.51/ 경도 126.12~126.68
jeju = (df['lat'] >= 33.16) & (df['lat'] <= 33.51) & \
            (df['lng'] >= 126.12) & (df['lng'] <= 126.68)
df_in = jeju.sum()
df_out = len(df) - df_in

print("'N'변경 전 :",df["theme"].unique())

df['theme'] = df['theme'].replace({'N': '기타'})

print("'N'변경 후:",df["theme"].unique())

print("테마 데이터별 개수:")
# 1. 모든 theme을 한 리스트로 풀어버리기
themes = []
for t in df['theme'].dropna():  # 결측치 제거
    for item in t.split(','):  # 쉼표로 자르기
        themes.append(item.strip())  # 공백 제거해서 추가
# 2. 개수 세기
from collections import Counter
counts = Counter(themes)
# 3. 출력
print(counts)

file_path2 = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/관광지_2.json"
df.to_json(file_path2, orient='records', indent=4, force_ascii=False)
df_food_street = df[df['theme'] == '먹거리/패션거리']
print(df_food_street["name"].head(10))

print(df[df['theme'] == '먹거리/패션거리'].head(10))

print("먹거리/패션거리 테마 데이터 개수:",len(df[df['theme'] == '먹거리/패션거리']))



