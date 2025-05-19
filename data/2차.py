import pandas as pd
import json

file_path = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/관광지_2.json"
with open(file_path,'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df['theme'].value_counts()) 
df.replace([pd.NA], "정보없음",
           inplace= True) 
print(df.head(14))

#저장 
file_path = "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/정보없음_관광지2.json"
df.to_json(file_path, orient='records', indent=4, force_ascii=False)

#theme 카테고리 통합. 
theme_mapping = {
    # 역사/문화유산
    '유명사적/유적지': '역사/문화유산',
    '보물': '역사/문화유산',
    '비/탑/문/각': '역사/문화유산',
    '고택/생가/민속마을': '역사/문화유산',
    '서원/향교/서당': '역사/문화유산',
    '성/성터': '역사/문화유산',
    '왕릉/고분': '역사/문화유산',

    # 자연경관
    '천연기념물': '자연경관',
    '해수욕장': '바다', #바다
    '폭포/계곡': '산', #바다
    '식물원': '자연경관',
    '휴양림/수목원': '자연경관',
    '온천지역': '자연경관',

    # 체험/레저
    '관광농원/허브마을':'체험/레저',
    '팜스테이': '체험/레저',
    '테마공원/대형놀이공원': '체험/레저',
    '일반유원지/일반놀이공원': '체험/레저',
    '야영장': '체험/레저',
    '캠핑장': '체험/레저',
    '캠핑홀리데이(캠핑)': '체험/레저',
    '드라마/영화촬영지': '체험/레저',
    '동물원': '체험/레저',
    '아쿠아리움/대형수족관': '체험/레저',
    '영어마을': '체험/레저',

    # 지역문화/이벤트
    '지역축제': '지역문화/이벤트',
    '정보화마을': '지역문화/이벤트',

    # 관광명소
    '일반관광지': '관광명소',
    '유명관광지': '관광명소',

    # 먹거리/쇼핑
    '먹거리/패션거리': '기타',

    # 편의시설
    '관광안내소/매표소': '관광안내소/매표소',

    # 기타
    'N': '기타'
} # 먹거리/패션거리 기타로
df["theme_category"] = df["theme"].replace(theme_mapping)
print(df.head(3))
file_path3= "C:/Users/82102/Desktop/HIU_travel-main/HIU_travel-main/data/테마카테고리통합(먹거리기타)_관광지2.json"
df.to_json(file_path3, orient='records', indent=4, force_ascii=False)
#음식점 통합. 

