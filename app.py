import streamlit as st


st.set_page_config(page_title="나만의 데이터 연구소", page_icon="🤖", layout="wide")

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

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

st.markdown(
    """
    <div style='color: black; font-size: 20px; text-align: right; margin-bottom: 6px;'>
        *대상학년: 고등학교 2~3학년
    </div>
    """,
    unsafe_allow_html=True
)

from PIL import Image

banner = Image.open("images/(1)main_banner.png")  
st.image(banner, use_container_width=True)   

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">📖 개념 익히기</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/1_경사하강법_(1)_최적화란.py", label="(1) 최적화란?")
        st.page_link("pages/2_경사하강법_(2)_학습률이란.py", label="(2) 학습률이란?")
        st.page_link("pages/3_경사하강법_(3)_반복횟수란.py", label="(3) 반복횟수란?")

with col2:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">💻 시뮬레이션</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/4_시뮬레이션_(1)_학습률_실험.py", label="(1) 학습률 실험")
        st.page_link("pages/5_시뮬레이션_(2)_반복횟수_실험.py", label="(2) 반복횟수 실험")

with col3:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">🔎 예제</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)

        st.markdown("""
            <a href="/example" target="_self" style="
                display: block;
                line-height: 1.4;
                word-break: keep-all;
                white-space: normal;
                color: inherit;
                text-decoration: none;
            ">
                Q. 나 혼자 산다!<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;다 혼자 산다?
            </a>
        """, unsafe_allow_html=True)




with col4:
    with st.container(border=True):
        st.markdown('<div class="card-title-custom">📊 데이터분석</div>', unsafe_allow_html=True)
        st.markdown('<hr class="card-divider-custom">', unsafe_allow_html=True)
        st.page_link("pages/7_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
        st.page_link("pages/8_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
        st.page_link("pages/9_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
        st.page_link("pages/10_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
        st.page_link("pages/11_데이터분석_(5)_요약결과.py", label="(5) 요약 결과")

st.markdown("---")
st.success("왼쪽 메뉴 또는 위 카드에서 원하는 항목을 선택해 학습을 시작하세요!")

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
