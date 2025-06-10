import streamlit as st
import streamlit as st


st.set_page_config(
    page_title="인공지능의 원리",
    page_icon="🤖",
    layout="centered"
)

# 🔒 자동 생성된 사이드바 메뉴 숨기기
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

st.title("📊 경사하강법 학습 시스템")
st.caption("인공지능의 원리를 시각적으로 체험하며 익혀보는 학습 플랫폼")

st.markdown("---")

st.subheader("📘 경사하강법 이론")
st.page_link("pages/1_📘_경사하강법_(1)_최적화란.py", label="경사하강법 (1) 최적화란?", icon="📘")
st.page_link("pages/2_📘_경사하강법_(2)_학습률이란.py", label="경사하강법 (2) 학습률이란?", icon="📘")
st.page_link("pages/3_📘_경사하강법_(3)_반복횟수란.py", label="경사하강법 (3) 반복횟수란?", icon="📘")

st.markdown("---")

st.subheader("📒 시뮬레이션 실험")
st.page_link("pages/4_📒_시뮬레이션_(1)_학습률_실험.py", label="시뮬레이션 (1) 학습률 실험", icon="📒")
st.page_link("pages/5_📒_시뮬레이션_(2)_반복횟수_실험.py", label="시뮬레이션 (2) 반복횟수 실험", icon="📒")

st.markdown("---")

st.subheader("📕 데이터분석 프로젝트")
st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="데이터분석 (1) 기본 정보 입력", icon="📕")
st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="데이터분석 (2) 분석 주제 선택", icon="📕")
st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="데이터분석 (3) 데이터 입력", icon="📕")
st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="데이터분석 (4) 예측 실행", icon="📕")
st.page_link("pages/10_📕_데이터분석_(5)_예측해석.py", label="데이터분석 (5) 예측 해석", icon="📕")
st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="데이터분석 (6) 요약 결과", icon="📕")

st.markdown("---")
st.success("왼쪽 메뉴 또는 위 버튼을 눌러 학습을 시작하세요!")


with st.sidebar:
    # 🏠 홈으로
    st.page_link("app.py", label="HOME", icon="🏠")
    st.markdown("---")

    st.markdown("## 🤖 경사하강법")
    st.page_link("pages/1_📘_경사하강법_(1)_최적화란.py", label="(1) 최적화란?")
    st.page_link("pages/2_📘_경사하강법_(2)_학습률이란.py", label="(2) 학습률이란?")
    st.page_link("pages/3_📘_경사하강법_(3)_반복횟수란.py", label="(3) 반복횟수란?")

    st.markdown("---")

    st.markdown("## 💻 시뮬레이션")
    st.page_link("pages/4_📒_시뮬레이션_(1)_학습률_실험.py", label="(1) 학습률 실험")
    st.page_link("pages/5_📒_시뮬레이션_(2)_반복횟수_실험.py", label="(2) 반복횟수 실험")

    st.markdown("---")

    st.markdown("## 📊 데이터분석")
    st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/10_📕_데이터분석_(5)_예측해석.py", label="(5) 예측 해석")
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(6) 요약 결과"
                 )
