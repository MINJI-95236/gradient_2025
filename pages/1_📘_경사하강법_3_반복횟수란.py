import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform

from matplotlib import font_manager

# 프로젝트 내 폰트 경로 등록
font_path = "./fonts/NotoSansKR-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Noto Sans KR"
plt.rcParams["axes.unicode_minus"] = False



st.title("📘 경사하강법 · 3단계: 반복횟수란?")

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
