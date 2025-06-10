import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform

from matplotlib import font_manager

# ✅ 페이지 메타 설정 (브라우저 탭 제목 및 아이콘)
st.set_page_config(
    page_title="📘 경사하강법 (2) 학습률이란?",
    page_icon="📘",
    layout="centered"
)
# 프로젝트 내 폰트 경로 등록
font_path = "./fonts/NotoSansKR-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Noto Sans KR"
plt.rcParams["axes.unicode_minus"] = False

# 🔒 자동 생성된 사이드바 메뉴 숨기기
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

st.title("📘 (2) 경사하강법-학습률")
col1, col2, col3 = st.columns([2, 7, 3])  # col3이 오른쪽 끝
with col3:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")  # 또는 정확한 페이지 경로
st.markdown("""
### 🧪 학습률(Learning Rate)이란?

- 경사하강법에서 **얼마만큼 이동할지 결정하는 값**이에요.
- 학습률이 너무 작으면 **너무 천천히 수렴**하고,  
  너무 크면 **최솟값을 지나쳐서 발산할 수 있어요.**

---

아래 그래프는 서로 다른 학습률이 어떤 이동을 만들어내는지 보여줍니다.
""")

# 예시 시각화
x = np.linspace(-2, 2, 100)
y = x**2

fig, ax = plt.subplots()
ax.plot(x, y, label="함수 y = x²", color="black")

# 학습률 예시 점
lr_steps = [-1.5, -1.0, -0.5]
ax.plot(lr_steps, [s**2 for s in lr_steps], "ro-", label="학습률 이동 예시")

ax.set_title("학습률에 따른 이동 예시")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
st.pyplot(fig)

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
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(6) 요약 결과")
