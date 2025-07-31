import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택",
    page_icon="📊",
    layout="centered"
)

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

banner = Image.open("images/(9)title_select_topic.png")  
st.image(banner, use_container_width=True)
with st.sidebar:
    st.page_link("app.py", label="HOME", icon="🏠")
    st.markdown("---")

    st.markdown("## 📖 개념 익히기")
    st.page_link("pages/1_경사하강법_(1)_최적화란.py", label="(1) 최적화란?")
    st.page_link("pages/2_경사하강법_(2)_학습률이란.py", label="(2) 학습률이란?")
    st.page_link("pages/3_경사하강법_(3)_반복횟수란.py", label="(3) 반복횟수란?")

    st.markdown("---")
    st.markdown("## 💻 시뮬레이션")
    st.page_link("pages/4_시뮬레이션_(1)_학습률_실험.py", label="(1) 학습률 실험")
    st.page_link("pages/5_시뮬레이션_(2)_반복횟수_실험.py", label="(2) 반복횟수 실험")

    st.markdown("---")
    st.markdown("## 🔎 예제")
    st.page_link("pages/6_example.py", label="Q. 나 혼자 산다! 다 혼자 산다?")

    st.markdown("---")
    st.markdown("## 📊 데이터분석")
    st.page_link("pages/7_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/8_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/9_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/10_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/11_데이터분석_(5)_요약결과.py", label="(5) 요약 결과")

if "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

subject = st.text_area(
    "📌 국가통계포털을 이용해 분석하고 싶은 데이터를 찾아보고, 주제를 작성하세요!",
    value=st.session_state.get("subject", ""),
    placeholder="예: 공부시간에 대한 성적 예측하기",
    key="input_subject"  
)
st.markdown("[🔎 국가통계포털 바로가기](https://kosis.kr/index/index.do)", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 1])
with col_left:
    with open("data/sample data.xlsx", "rb") as file:
        st.download_button(
            label="📥 예시 주제 및 데이터 다운로드",
            data=file,
            file_name="2008~2022년의 인구 1000명당 병상수.xlsx",
            mime="text/csv"
        )

with col_right:
    if st.button("✅ 주제 저장", use_container_width=True):
        if subject.strip():
            st.session_state.subject = subject
            st.session_state.subject_saved = True
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

if st.session_state.get("subject_saved"):
    st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")


if "subject" in st.session_state:
    col1, col2, col3 = st.columns([3, 15, 3])
    with col1:
        if st.button("⬅️ 이전"):
            st.switch_page("pages/7_데이터분석_(1)_기본정보입력.py")
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/9_데이터분석_(3)_데이터입력.py")



