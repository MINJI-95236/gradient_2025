import streamlit as st

st.set_page_config(
    page_title="인공지능의 원리",
    page_icon="🤖",
    layout="centered"
)

st.title("📊 경사하강법 학습 시스템")
st.caption("인공지능의 원리를 시각적으로 체험하며 익혀보는 학습 플랫폼")

st.markdown("---")

st.subheader("📘 1단원: 경사하강법 이론")
st.page_link("pages/1_📘_경사하강법_1_최적화란.py", label="1-1. 최적화란?", icon="📘")
st.page_link("pages/1_📘_경사하강법_2_학습률이란.py", label="1-2. 학습률이란?", icon="📘")
st.page_link("pages/1_📘_경사하강법_3_반복횟수란.py", label="1-3. 반복횟수란?", icon="📘")

st.markdown("---")

st.subheader("🧪 2단원: 실습")
st.page_link("pages/2_🧪_학습률_실습.py", label="2-1. 학습률 실습", icon="🧪")
st.page_link("pages/3_🔁_반복횟수_실습.py", label="2-2. 반복횟수 실습", icon="🔁")

st.markdown("---")

st.subheader("📊 3단원: 데이터 분석 프로젝트")
st.page_link("pages/4_1️⃣_정보입력.py", label="4-1. 정보 입력", icon="1️⃣")
st.page_link("pages/4_2️⃣_분석주제.py", label="4-2. 분석주제", icon="2️⃣")
st.page_link("pages/4_3️⃣_데이터 입력.py", label="4-3. 데이터 입력", icon="3️⃣")
st.page_link("pages/4_4️⃣_예측결과.py", label="4-4. 예측 결과", icon="4️⃣")
st.page_link("pages/4_5️⃣_예측입력.py", label="4-5. 예측 입력", icon="5️⃣")

st.markdown("---")
st.success("왼쪽 메뉴 또는 위 버튼을 눌러 학습을 시작하세요!")
