# 제주 관광지 추천 시스템

본 프로젝트는 Streamlit을 기반으로 한 제주도 관광지 추천 웹 애플리케이션입니다. 사용자가 선택한 테마와 음식 카테고리를 바탕으로 당일치기 또는 숙박 일정에 따라 관광지, 음식점, 카페를 경로 기반으로 추천합니다.

---

## 🔧 가상환경 설정 및 설치 패키지 안내

이 프로젝트는 Python 기반의 Streamlit 웹 애플리케이션입니다. 원활한 실행을 위해 별도의 가상환경을 구성하고 필요한 라이브러리를 설치해야 합니다. 아래 안내를 따라 실행 환경을 구성하세요.

### 1️⃣ 가상환경 생성 및 활성화

Python 3.10 이상 환경을 권장합니다.

#### (1) Anaconda를 사용하는 경우:

```bash
conda create -n jeju python=3.10
conda activate jeju
```

#### (2) venv를 사용하는 경우:

```bash
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

---

### 2️⃣ 필수 패키지 설치

requirements.txt 파일이 있다면 아래 명령어로 한 번에 설치할 수 있습니다:

```bash
pip install -r requirements.txt
```

requirements.txt 파일이 없다면, 아래 명령어로 직접 설치할 수 있습니다:

```bash
pip install streamlit pandas geopy folium streamlit-folium
```

---

### 3️⃣ 프로젝트 실행

가상환경이 활성화된 상태에서 아래 명령어를 실행하면 웹 애플리케이션이 브라우저에서 열립니다:

```bash
streamlit run app.py
```

> ⚠️ 실행 파일명이 `app.py`가 아니라면, 실제 파일명으로 바꿔서 실행하세요.

---

## 📁 폴더 구조

```
project-root/
├── app.py
├── DB/
│   ├── jejudb.db
│   └── 0608_카페음식점분류 데이터.csv
├── README.md
└── requirements.txt
```

---
