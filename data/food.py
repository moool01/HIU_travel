import pandas as pd    
import json 

file_path = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/음식점_통합.csv"

food= pd.read_csv(file_path)
food.info
print(food.isnull().sum())
# 결측치 비율 계산
missing_ratio = food.isnull().mean() * 100

# 결측치 비율을 내림차순으로 정렬해서 출력
print(missing_ratio.sort_values(ascending=False))

#1. 98%이상인 결측치 삭제
drops  = missing_ratio[missing_ratio > 98].index 
food = food.drop(columns=drops)

#다시 결측치 비율 찾기.
missing_ratio = food.isnull().mean() * 100
# 결측치 비율을 내림차순으로 정렬해서 출력
print(missing_ratio.sort_values(ascending=False))

# 2. 둘 중 하나라도 값이 있으면 상호 보완하여 결측치를 채움.
# 전화번호와 문의 및 안내는 똑같은 내용이 대부분인데,  [전화번호는 결측치가  76.285047이고, 문의 및 안내는 0.467290이다.] 
#어느 하나라도 있으면 그걸로 채우는 거 필요.
print("1: 전화번호에 문의 및 안내 채우기")
food['전화번호'] = food['전화번호'].fillna(food['문의 및 안내'])
print("2: 문의 및 안내에 전화번호 채우기")
food['문의 및 안내'] = food['문의 및 안내'].fillna(food['전화번호'])

print(food.isnull().sum())
missing_ratio2 = food.isnull().mean() * 100
print(missing_ratio2.sort_values(ascending = False))

#3. 불필요한 컬럼 [인허가 번호, 문의 및 안내] 지우기
food = food.drop(['문의 및 안내','인허가번호'],axis=1)
print(food.head())

#지금까지 거 
file_path = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/food.csv"
food.to_csv(file_path, index=False, encoding='utf-8-sig')

#중복 데이터 확인하기 
print(food.duplicated().sum()) #중복데이터는 없다.

print(food['대표메뉴'].unique())