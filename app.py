import streamlit as st

st.set_page_config(page_title="인공지능의 원리", page_icon="🤖", layout="wide")

# ✅ 기본 사이드바 메뉴 숨기기 + 카드 스타일 CSS 삽입
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }

    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        border: 1px solid #ccc;
        margin-bottom: 20px;
        transition: transform 0.1s ease;
    }
    .card:hover {
        transform: translateY(-2px);  /* 약간 튀어나오게 */
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }
    .card h3 {
        margin-top: 4px;
        color: black;
        font-size: 20px;
        margin-bottom: 4px;
    }
    .card hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2px 0 11px 0;  /* 위 4px, 아래 8px */
    }
    .card ul {
        list-style-type: none;
        padding-left: 0;
    }

    .card li {
        margin: 6px 0;
    }

    .card a {
        text-decoration: none;
        color: #333;
        font-size: 16px;
    }

    .card a:hover {
        color: #007acc;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 타이틀 및 안내
st.title("📊 경사하강법 학습 시스템")
st.caption("인공지능의 원리를 시각적으로 체험하며 익혀보는 학습 플랫폼")
#st.markdown("---")

# ✅ 카드형 3단 구성
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📘 경사하강법 이론</h3>
        <hr>            
        <ul>
            <li><a href="/pages/1_📘_경사하강법_(1)_최적화란.py">(1) 최적화란?</a></li>
            <li><a href="/pages/2_📘_경사하강법_(2)_학습률이란.py">(2) 학습률이란?</a></li>
            <li><a href="/pages/3_📘_경사하강법_(3)_반복횟수란.py">(3) 반복횟수란?</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📒 시뮬레이션 실험</h3>
        <hr>
        <ul>
            <li><a href="/pages/4_📒_시뮬레이션_(1)_학습률_실험.py">(1) 학습률 실험</a></li>
            <li><a href="/pages/5_📒_시뮬레이션_(2)_반복횟수_실험.py">(2) 반복횟수 실험</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>📕 데이터분석 프로젝트</h3>
        <hr>
        <ul>
            <li><a href="/pages/6_📕_데이터분석_(1)_기본정보입력.py">(1) 기본 정보 입력</a></li>
            <li><a href="/pages/7_📕_데이터분석_(2)_분석주제선택.py">(2) 분석 주제 선택</a></li>
            <li><a href="/pages/8_📕_데이터분석_(3)_데이터입력.py">(3) 데이터 입력</a></li>
            <li><a href="/pages/9_📕_데이터분석_(4)_예측실행.py">(4) 예측 실행</a></li>
            <li><a href="/pages/10_📕_데이터분석_(5)_예측해석.py">(5) 예측 해석</a></li>
            <li><a href="/pages/11_📕_데이터분석_(6)_요약결과.py">(6) 요약 결과</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ✅ 안내 메시지
st.markdown("---")
st.success("왼쪽 메뉴 또는 위 카드에서 원하는 항목을 선택해 학습을 시작하세요!")

# ✅ 사이드바 (기존 유지)
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
    st.markdown("## 📊 데이터분석")
    st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/10_📕_데이터분석_(5)_예측해석.py", label="(5) 예측 해석")
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(6) 요약 결과")
