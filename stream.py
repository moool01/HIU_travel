# streamlit_app.py
import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import sqlite3

# 1. 데이터 로딩
@st.cache_data
def load_data():
    conn = sqlite3.connect("DB/jejudb.db")
    df = pd.read_sql("SELECT * FROM tour", conn)
    conn.close()
    return df

data = load_data()

st.title("📍 제주 관광지 추천 데모")

# 고정 안내 문구
st.markdown("**현재 위치는 _제주국제공항(Jeju International Airport)_ 으로 고정되어 있습니다.**")

# 내부적으로 사용할 위경도 (사용자에겐 보이지 않음)
lat = 33.499621
lng = 126.531188

category = st.selectbox(
    "선호하는 관광 카테고리를 선택하세요",
    options=data["theme"].unique()
)

# 3. 추천 로직
def recommend_place(lat, lng, selected_theme, top_n=5):
    candidates = data.copy()

    # 거리 계산
    candidates["거리_km"] = candidates.apply(
        lambda row: geodesic((lat, lng), (row["lat"], row["lng"])).km, axis=1
    )
    max_dist = candidates["거리_km"].max()

    # 선택한 theme의 theme_category를 찾기
    selected_theme_category = data.loc[data["theme"] == selected_theme, "theme_category"].iloc[0]

    # 콘텐츠 점수 계산
    def content_score(row):
        if row["theme"] == selected_theme:
            return 0.2
        elif row["theme_category"] == selected_theme_category:
            return 0.1
        else:
            return 0.0

    candidates["콘텐츠점수"] = candidates.apply(content_score, axis=1)

    # 거리 점수 계산
    candidates["거리점수"] = (1 - candidates["거리_km"] / max_dist) * 0.8
    candidates["거리점수"] = candidates["거리점수"].clip(lower=0.0)

    # 최종 점수
    candidates["최종점수"] = candidates["콘텐츠점수"] + candidates["거리점수"]

    return candidates.sort_values(by="최종점수", ascending=False).head(top_n)

if st.button("추천받기"):
    if "lat" in data.columns and "lng" in data.columns:
        recommendations = recommend_place(lat, lng, category)
        st.success(f"🎯 '{category}' 관련 추천 장소입니다:")
        st.dataframe(recommendations[["name", "theme", "theme_category", "거리_km", "최종점수"]])
    else:
        st.error("⚠️ 위도/경도 정보가 데이터에 없습니다.")