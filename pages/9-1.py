import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import platform
import os
import matplotlib.font_manager as fm

# ✅ 한글 폰트 설정
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
else:
    plt.rcParams["font.family"] = "AppleGothic" if platform.system() == "Darwin" else "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ✅ 페이지 설정
st.set_page_config(page_title="📕 데이터분석 (4) 예측 실행 - 단일", layout="wide")
st.title("📕 (4) 예측 실행")

# ✅ 데이터 불러오기
if "x_values" not in st.session_state or "y_values" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

x_raw = np.array(st.session_state.x_values)
y_raw = np.array(st.session_state.y_values)
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# ✅ 함수 형태 선택
func_type = st.radio("🔢 함수 형태를 선택하세요:", ["1차 함수", "2차 함수"])

# ✅ 학습률, 반복 횟수 선택
col1, col2 = st.columns(2)
with col1:
    learning_rate = st.slider("📘 학습률을 선택하세요:", min_value=0.0001, max_value=0.0050, value=0.0001, step=0.0001, format="%.4f")
    st.markdown(f"👉 현재 학습률: `{learning_rate}` <br> 🔍 너무 크면 발산할 수 있어요", unsafe_allow_html=True)
with col2:
    epoch = st.slider("🔁 반복 횟수를 선택하세요:", min_value=100, max_value=5000, value=1000, step=100)
    st.markdown(f"👉 현재 반복 횟수: `{epoch}`회 <br> 📈 충분한 반복은 정확도를 높일 수 있어요", unsafe_allow_html=True)

# ✅ 예측 실행
if st.button("📈 예측 그래프 그리기"):
    x = x_raw
    y = y_raw

    if func_type == "1차 함수":
        x_mean = x.mean()
        x_centered = x - x_mean
        m, b = 0.0, 0.0
        n = len(x)
        for _ in range(epoch):
            y_pred = m * x_centered + b
            error = y_pred - y
            m -= learning_rate * (2 / n) * np.dot(error, x_centered)
            b -= learning_rate * (2 / n) * error.sum()
        m_real = m
        b_real = b - m * x_mean
        y_pred_full = m_real * x + b_real
        x_plot = np.linspace(x.min(), x.max(), 100)
        y_plot = m_real * x_plot + b_real
        latex_eq = f"y = {m_real:.4f} \\times x {'-' if b_real < 0 else '+'} {abs(b_real):.2f}"
        predict_fn = lambda x_input: m_real * x_input + b_real

    else:
        x_mean = x.mean()
        x_std = x.std()
        x_scaled = (x - x_mean) / x_std
        a, b, c = 0.0, 0.0, 0.0
        n = len(x)
        for _ in range(epoch):
            y_pred = a * x_scaled**2 + b * x_scaled + c
            error = y_pred - y
            a -= learning_rate * (2 / n) * np.dot(error, x_scaled**2)
            b -= learning_rate * (2 / n) * np.dot(error, x_scaled)
            c -= learning_rate * (2 / n) * error.sum()
        a_real = a / (x_std**2)
        b_real = (-2 * a * x_mean / (x_std**2)) + (b / x_std)
        c_real = (a * x_mean**2 / (x_std**2)) - (b * x_mean / x_std) + c
        y_pred_full = a_real * x**2 + b_real * x + c_real
        x_plot = np.linspace(x.min(), x.max(), 100)
        y_plot = a_real * x_plot**2 + b_real * x_plot + c_real
        latex_eq = (
            f"y = {a_real:.4f} x^2 "
            f"{'+' if b_real >= 0 else '-'} {abs(b_real):.4f} x "
            f"{'+' if c_real >= 0 else '-'} {abs(c_real):.4f}"
        )
        predict_fn = lambda x_input: a_real * x_input**2 + b_real * x_input + c_real

    # 🎯 정확도 계산
    ss_res = np.sum((y - y_pred_full) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    accuracy = r2 * 100

    # 📊 결과 시각화
    st.markdown("## 4️⃣ 예측 결과")
    colL, colR = st.columns([2, 1])
    with colL:
        fig, ax = plt.subplots()
        ax.scatter(x, y, color="blue", label="실제값")
        ax.plot(x_plot, y_plot, color="red", label="예측값")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("예측 결과")
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        st.pyplot(fig)

    with colR:
        st.markdown("### 📌 예측 수식")
        st.latex(latex_eq)
        st.write(f"반복 횟수: `{epoch}`회")
        st.write(f"학습률: `{learning_rate}`")

        input_x = st.number_input("예측하고 싶은 값을 입력하세요. (예: 연도, 나이, 기온 등)", value=int(x[-1])+1, step=1)
        y_future = predict_fn(input_x)
        st.markdown(f"📅 **입력값이 `{input_x}`일 때**, 예측 결과는 **`{y_future:.1f}`**입니다.")
        st.metric("🎯 모델 정확도", f"{accuracy:.2f} %")
