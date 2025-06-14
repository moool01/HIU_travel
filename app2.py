import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import sqlite3
import random
import folium
from streamlit_folium import st_folium

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

airport_lat = tour_data["lat"].mean()
airport_lng = tour_data["lng"].mean()

st.title("제주 관광지 추천 데모")

all_themes = sorted(tour_data["theme"].dropna().unique())
selected_themes = st.multiselect("해당 관광 테마 선택", all_themes, max_selections=4)

all_categories = sorted(restaurant_data["대분류"].dropna().unique())
selected_categories = st.multiselect("음식 카테고리 선택", all_categories, max_selections=2)

day_options = {"1일 내": 1, "1박 2일": 2, "2박 3일": 3}
selected_day_option = st.radio("여행 일수를 선택해주세요", list(day_options.keys()))
days = day_options[selected_day_option]

if st.button("추천 시작하기"):
    st.session_state.trigger = True

if st.session_state.get("trigger", False):

    def recommend_places(lat, lng, themes, top_n=1, used_places=[], use_distance=True):
        candidates = tour_data.copy()
        candidates = candidates[~candidates["name"].isin(used_places)]
        candidates["거리_km"] = candidates.apply(lambda row: geodesic((lat, lng), (row["lat"], row["lng"])).km, axis=1)
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

        if use_distance:
            max_dist = candidates["거리_km"].max()
            candidates["거리점수"] = (1 - candidates["거리_km"] / max_dist) * 0.5
            candidates["최종점수"] = candidates["콘텐츠점수"] + candidates["거리점수"]
        else:
            rand_scale = random.uniform(0.0, 0.5)
            candidates["최종점수"] = candidates["콘텐츠점수"] + (1 - rand_scale)

        return candidates.sort_values(by="최종점수", ascending=False).head(top_n)

    def recommend_restaurants(lat, lng, categories, top_n=1):
        candidates = restaurant_data.copy()
        if categories == ["카페"]:
            candidates = candidates[candidates["카페/음식점"] == "카페"]
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
        candidates = candidates[candidates["거리_km"] <= 5]
        return candidates.sort_values(by="거리_km").head(top_n)

    def show_map_multiple_days(all_day_points):
        if not all_day_points:
            st.warning("경로 정보가 없습니다.")
            return

        m = folium.Map(location=all_day_points[0][0][0:2], zoom_start=10, tiles="CartoDB positron")

        color_cycle = ["blue", "green", "purple", "red", "orange"]
        for i, points in enumerate(all_day_points):
            day_color = color_cycle[i % len(color_cycle)]
            for j, (lat, lng, label) in enumerate(points):
                folium.Marker(
                    location=[lat, lng],
                    popup=f"Day {i+1} - {label}",
                    icon=folium.Icon(color=day_color)
                ).add_to(m)
            folium.PolyLine([(lat, lng) for lat, lng, _ in points], color=day_color, weight=3, opacity=0.8).add_to(m)

        st.markdown("### 🗺️ 전체 일정 경로 지도")
        st_folium(m, width=800, height=600)

    lat, lng = airport_lat, airport_lng
    used_places = []
    all_day_points = []

    for i in range(days):
        tour1 = recommend_places(lat, lng, selected_themes, used_places=used_places, use_distance=False)
        if tour1.empty:
            st.warning(f"{i+1}일차 추천 실패")
            break
        top_tour = tour1.iloc[0]
        used_places.append(top_tour["name"])

        food = recommend_restaurants(top_tour["lat"], top_tour["lng"], selected_categories)
        if food.empty:
            st.warning("음식점 추천 실패")
            break
        top_food = food.iloc[0]

        cafe = recommend_restaurants(top_food["위도"], top_food["경도"], ["카페"])
        if cafe.empty:
            st.warning("카페 추천 실패")
            break
        top_cafe = cafe.iloc[0]

        tour2 = recommend_places(top_food["위도"], top_food["경도"], selected_themes, used_places=used_places)
        if not tour2.empty:
            second_tour = tour2.iloc[0]
            used_places.append(second_tour["name"])
        else:
            second_tour = top_tour

        st.subheader(f"Day {i+1} 일정")
        st.dataframe(pd.DataFrame([top_tour]))
        st.dataframe(pd.DataFrame([top_food]))
        st.dataframe(pd.DataFrame([top_cafe]))
        st.dataframe(pd.DataFrame([second_tour]))

        points = [
            (top_tour["lat"], top_tour["lng"], "1차 관광지"),
            (top_food["위도"], top_food["경도"], "2차 음식점"),
            (top_cafe["위도"], top_cafe["경도"], "3차 카페"),
            (second_tour["lat"], second_tour["lng"], "4차 관광지")
        ]
        all_day_points.append(points)

        lat, lng = second_tour["lat"], second_tour["lng"]

    show_map_multiple_days(all_day_points)