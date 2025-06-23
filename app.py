import streamlit as st

st.set_page_config(page_title="인공지능의 원리", page_icon="🤖", layout="wide")

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

# ✅ 카드 제목 여백 조절을 위한 CSS
st.markdown("""
    <style>
    .card-title-custom {
        font-size: 20px;
        font-weight: 600;
        margin-top: 0px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .card-divider-custom {
        border: none;
        border-top: 1px solid #ccc;
        margin: 2px 0 6px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 메인 타이틀
st.title("📊 경사하강법 학습 시스템")
st.caption("인공지능의 원리를 시각적으로 체험하며 익혀보는 학습 플랫폼")
st.markdown("---")

# ✅ 카드형 4단 구성 (예제를 데이터분석보다 앞에 위치)
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">🤖 경사하강법</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/1_📘_경사하강법_(1)_최적화란.py", label="(1) 최적화란?")
        st.page_link("pages/2_📘_경사하강법_(2)_학습률이란.py", label="(2) 학습률이란?")
        st.page_link("pages/3_📘_경사하강법_(3)_반복횟수란.py", label="(3) 반복횟수란?")

with col2:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">💻 시뮬레이션</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/4_📒_시뮬레이션_(1)_학습률_실험.py", label="(1) 학습률 실험")
        st.page_link("pages/5_📒_시뮬레이션_(2)_반복횟수_실험.py", label="(2) 반복횟수 실험")

with col3:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">🍧 예제</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)

        st.markdown(
            """
            <a href="/5_1_example_icecream_prediction" target="_self" style="
                display: block;
                font-weight: 500;
                line-height: 1.6;
                margin-bottom: 12px;
                color: inherit;
                text-decoration: none;
                cursor: pointer;
            ">
                Q. 나 혼자 산다!<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;다 혼자 산다?
            </a>
            """,
            unsafe_allow_html=True
        )



with col4:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">📊 데이터분석</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
        st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
        st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
        st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
        st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(5) 요약 결과")

# ✅ 안내 메시지
st.markdown("---")
st.success("왼쪽 메뉴 또는 위 카드에서 원하는 항목을 선택해 학습을 시작하세요!")

# ✅ 사이드바 구성 (예제를 데이터분석보다 위로 정렬)
with st.sidebar:
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
    st.markdown("## 🍧 예제")
    st.page_link("pages/_5_1_example_icecream_prediction.py", label="Q. 나 혼자 산다! 다 혼자 산다?")

    st.markdown("---")
    st.markdown("## 📊 데이터분석")
    st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(5) 요약 결과")
