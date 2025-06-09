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
