
import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import sqlite3

# -----------------------------
# 🔹 데이터 로드
# -----------------------------
@st.cache_data
def load_tour_data():
    conn = sqlite3.connect("DB/jejudb.db")
    df = pd.read_sql("SELECT * FROM tour", conn)
    conn.close()
    return df

@st.cache_data
def load_restaurant_data():
    return pd.read_csv("DB/0608_카페음식점분류 데이터.csv", encoding='cp949')

tour_data = load_tour_data()
restaurant_data = load_restaurant_data()

# -----------------------------
# 🔹 기본 설정
# -----------------------------
airport_lat = tour_data["lat"].mean()
airport_lng = tour_data["lng"].mean()

# -----------------------------
# 🌟 출력 UI: 관광지-음식점-카페-새로운 관광지
# -----------------------------
st.title("제주 관광지 추천 데모")

# st.markdown("**현재 위치는 _산중앙_으로 고정되어 있습니다.**")

# 1. 관광지 테마 선택
all_themes = sorted(tour_data["theme"].dropna().unique())
selected_themes = st.multiselect("해당 관광 테마 선택", all_themes, max_selections=4)

# 2. 음식점 카테고리 선택
all_categories = sorted(restaurant_data["대분류"].dropna().unique())
selected_categories = st.multiselect("음식 카테고리 선택", all_categories,max_selections=2)

# -----------------------------
# 추천 함수들
# -----------------------------
def recommend_places(lat, lng, themes, top_n=1):
    candidates = tour_data.copy()
    candidates["거리_km"] = candidates.apply(lambda row: geodesic((lat, lng), (row["lat"], row["lng"])).km, axis=1)
    max_dist = candidates["거리_km"].max()

    if not themes:
        return pd.DataFrame()

    theme_weights = {t: 1 / len(themes) for t in themes}

    def content_score(row):
        score = 0.0
        for theme in themes:
            cat = tour_data.loc[tour_data["theme"] == theme, "theme_category"].iloc[0]
            if row["theme"] == theme:
                score += 0.5 * theme_weights[theme]
            elif row["theme_category"] == cat:
                score += 0.25 * theme_weights[theme]
        return score

    candidates["콘텐츠점수"] = candidates.apply(content_score, axis=1)
    candidates["거리점수"] = (1 - candidates["거리_km"] / max_dist) * 0.5
    candidates["최종점수"] = candidates["콘텐츠점수"] + candidates["거리점수"]
    return candidates.sort_values(by="최종점수", ascending=False).head(top_n)

def recommend_restaurants(lat, lng, categories, top_n=1):
    candidates = restaurant_data.copy()

    # 카페 추천의 경우: 대분류가 '카페/음식점'이고, 소분류 또는 명칭에 '카페' 포함된 것만 필터링
    if categories == ["카페"]:
        candidates = candidates[
            (candidates["카페/음식점"] == "카페")
        ]
    elif categories:
        candidates = candidates[candidates["대분류"].isin(categories)]
    else:
        return pd.DataFrame()

    def compute_distance(row):
        try:
            return geodesic((lat, lng), (row["위도"], row["경도"])).km
        except:
            return float('inf')

    candidates["거리_km"] = candidates.apply(compute_distance, axis=1)
    return candidates.sort_values(by="거리_km").head(top_n)

# -----------------------------
# 추천 시작 버튼
# -----------------------------
if st.button("추천 시작하기"):
    # Step 1: 관광지
    tour_result = recommend_places(airport_lat, airport_lng, selected_themes)
    if tour_result.empty:
        st.warning("관광지 추천 결과가 없습니다.")
    else:
        top_tour = tour_result.iloc[0]
        st.session_state["top_tour"] = top_tour
        st.success(f"📍 1차 관광지: {top_tour['name']}")
        st.dataframe(tour_result[["name", "theme", "theme_category", "address", "거리_km"]])

        # Step 2: 음식점
        food_result = recommend_restaurants(top_tour["lat"], top_tour["lng"], selected_categories)
        if food_result.empty:
            st.warning("음식점 추천 결과가 없습니다.")
        else:
            top_food = food_result.iloc[0]
            st.session_state["top_food"] = top_food
            st.success(f"🍽️ 2차 음식점: {top_food['명칭']}")
            st.dataframe(food_result[["명칭", "대분류","주소", "거리_km"]])

            # Step 3: 카페
            cafe_result = recommend_restaurants(top_food["위도"], top_food["경도"], ["카페"])
            if cafe_result.empty:
                st.warning("카페 추천 결과가 없습니다.")
            else:
                top_cafe = cafe_result.iloc[0]
                st.success(f"☕ 3차 카페: {top_cafe['명칭']}")
                st.dataframe(cafe_result[["명칭", "대분류", "주소", "거리_km"]])

                # Step 4: 다음 관광지 추천 (최초 테마 제외)
                remaining_themes = [t for t in all_themes if t not in selected_themes]
                tour_result2 = recommend_places(top_food["위도"], top_food["경도"], remaining_themes)
                if tour_result2.empty:
                    st.warning("새로운 관광지 추천 결과가 없습니다.")
                else:
                    st.success(f"🗺️ 4차 관광지 (new theme): {tour_result2.iloc[0]['name']}")
                    st.dataframe(tour_result2[["name", "theme", "theme_category", "address", "거리_km"]])

