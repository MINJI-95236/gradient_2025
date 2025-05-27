import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import numpy as np

# ✅ 한글 폰트 설정 (서버 포함)
try:
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    font_name = fm.FontProperties(fname=font_path).get_name()
    matplotlib.rc("font", family=font_name)
except:
    if platform.system() == "Windows":
        matplotlib.rc("font", family="Malgun Gothic")
    elif platform.system() == "Darwin":
        matplotlib.rc("font", family="AppleGothic")
    else:
        matplotlib.rc("font", family="DejaVu Sans")
matplotlib.rcParams["axes.unicode_minus"] = False

st.title("📈 4단계: 예측 결과")

# 🔒 이전 단계 데이터 확인
if "x_values" not in st.session_state or "y_values" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# ✅ 변수 설정
x_raw = st.session_state.x_values
y_raw = st.session_state.y_values
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# 📌 예측 파라미터 선택
func_type = st.radio("🔢 함수 형태를 선택하세요:", ["1차 함수", "2차 함수"])
learning_rate = st.selectbox("📘 학습률을 선택하세요:", [0.0001,0.001, 0.01, 0.1])
epoch = st.selectbox("🔁 반복 횟수를 선택하세요:", [100, 500, 1000, 5000])

# 📊 누적 그래프를 저장할 리스트
if "history" not in st.session_state:
    st.session_state.history = []

# 📉 경사하강법 함수 정의
def gradient_descent_linear(x, y, lr, epochs):
    m, b = 0.0, 0.0
    n = len(x)
    for _ in range(epochs):
        y_pred = m * x + b
        error = y_pred - y
        m -= lr * (2 / n) * (error @ x)
        b -= lr * (2 / n) * error.sum()
    return m, b

def gradient_descent_quadratic(x, y, lr, epochs):
    a, b, c = 0.0, 0.0, 0.0
    n = len(x)
    for _ in range(epochs):
        y_pred = a * x**2 + b * x + c
        error = y_pred - y
        a -= lr * (2 / n) * (error @ (x**2))
        b -= lr * (2 / n) * (error @ x)
        c -= lr * (2 / n) * error.sum()
    return a, b, c

# 🎯 산점도 누적 예측 실행
if st.button("📈 예측 실행"):
    x = np.array(x_raw)
    y = np.array(y_raw)

    x_mean = x.mean()
    x_centered = x - x_mean
    x_plot = np.linspace(x.min(), x.max(), 100)
    x_input = x_plot - x_mean

    if func_type == "1차 함수":
        m, b = gradient_descent_linear(x_centered, y, learning_rate, epoch)
        y_pred = m * x_input + b
        equation = f"y = {m:.4f}x + {b:.4f}"
    else:
        a, b, c = gradient_descent_quadratic(x_centered, y, learning_rate, epoch)
        y_pred = a * x_input**2 + b * x_input + c
        equation = f"y = {a:.4f}x² + {b:.4f}x + {c:.4f}"

    # 🔐 방어 코드: nan 또는 inf 방지
    if np.any(np.isnan(y_pred)) or np.any(np.isinf(y_pred)):
        st.error("❌ 예측 도중 오류가 발생했습니다. 학습률을 낮추거나 반복 횟수를 줄여보세요.")
        st.stop()

    st.session_state.history.append({
        "x_plot": x_plot,
        "y_pred": y_pred,
        "label": equation,
        "lr": learning_rate,
        "epoch": epoch,
        "x_mean": x_mean
    })

# 📊 누적 그래프 출력 (각각의 그래프 따로)
for i, run in enumerate(st.session_state.history):
    st.markdown(f"### 🔍 예측 {i+1}")
    fig, ax = plt.subplots()
    ax.scatter(x_raw, y_raw, color="blue", label="입력 데이터")
    ax.plot(run["x_plot"], run["y_pred"], color="red", label="예측선")
    ax.set_title(f"예측 결과 {i+1}")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
    if all(float(x).is_integer() for x in x_raw):
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    else:
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    st.pyplot(fig)

    st.markdown(
    f"""
    ✅ 예측이 완료되었습니다!  
    📌 **수식**: {run['label']}  
    📘 **학습률**: {run['lr']}  
    🔁 **반복 횟수**: {run['epoch']}
    """
)

# 다음 페이지로 이동
if st.session_state.history:
    display_options = [f"예측 {i+1}: {run['label']}" for i, run in enumerate(st.session_state.history)]
    selected = st.multiselect("📌 다음 단계로 보낼 예측선을 선택하세요:", options=display_options)
    if st.button("➡️ 다음 단계로 이동") and selected:
        selected_indices = [display_options.index(s) for s in selected]
        st.session_state.selected_model_indices = selected_indices
        st.switch_page("pages/5_5️⃣_예측입력.py")

