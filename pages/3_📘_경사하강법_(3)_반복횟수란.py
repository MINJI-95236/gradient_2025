import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform

from matplotlib import font_manager

st.set_page_config(
    page_title="📘 경사하강법 (3) 반복횟수란?",
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

st.title("📘 (2) 경사하강법-반복횟수")
col1, col2, col3 = st.columns([2, 7, 3])  # col3이 오른쪽 끝
with col3:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")  # 또는 정확한 페이지 경로

st.markdown("""
### 🔁 반복횟수(Epochs)란?

- 경사하강법은 여러 번 반복하며 최적값을 찾아가요.
- 한 번의 반복에서 경사를 따라 이동하고,  
  이 과정을 **여러 번 반복**할수록 더 좋은 결과를 얻을 수 있어요.

---

아래 그래프는 반복횟수(epoch)에 따라 예측선이 어떻게 변하는지를 보여줍니다.
""")

# 데이터 및 함수 정의
np.random.seed(42)
x = np.linspace(1, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 1, size=len(x))

x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_plot = x_input - x_mean

def gradient_descent(x, y, lr, epochs):
    m, b = 0, 0
    n = len(x)
    for _ in range(epochs):
        y_pred = m * x + b
        dm = (-2/n) * sum(x * (y - y_pred))
        db = (-2/n) * sum(y - y_pred)
        m -= lr * dm
        b -= lr * db
    return m, b

# 반복횟수별 결과 시각화
learning_rate = 0.001  # 고정 학습률
epoch_list = [1, 10, 100, 1000]

fig, ax = plt.subplots()
ax.scatter(x, y, color="black", label="입력 데이터")

for epoch in epoch_list:
    m, b = gradient_descent(x_centered, y, learning_rate, epoch)
    y_pred = m * x_input + b
    ax.plot(x_plot + x_mean, y_pred, label=f"{epoch}회 반복")

ax.set_title("반복횟수에 따른 예측선 변화")
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
    st.markdown("## 🏠 예제")
    st.page_link("pages/_5_1_example_icecream_prediction.py", label="Q. 나 혼자 산다! 다 혼자 산다?")
    
    st.markdown("---")

    st.markdown("## 📊 데이터분석")
    st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/10_📕_데이터분석_(5)_예측해석.py", label="(5) 예측 해석")
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(6) 요약 결과")
