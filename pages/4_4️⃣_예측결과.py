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

# 포함 검사
if "x_values" not in st.session_state or "y_values" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

x_raw = st.session_state.x_values
y_raw = st.session_state.y_values
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# 예측 파래미터 선택
func_type = st.radio("🔢 함수 형태를 선택하세요:", ["1차 함수", "2차 함수"])
learning_rate = st.selectbox("📘 학습률을 선택하세요:", [0.0001, 0.001, 0.01, 0.1])
epoch = st.selectbox("🔁 반복 횟수를 선택하세요:", [100, 500, 1000, 5000])

if "history" not in st.session_state:
    st.session_state.history = []

# 경상하견법 가설

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

    if np.any(np.isnan(y_pred)) or np.any(np.isinf(y_pred)):
        st.error("❌ 예측 동안 오류가 발생했습니다. 학습률을 낮이거나 반복 횟수를 줄어보세요.")
        st.stop()

    st.session_state.history.append({
        "x_plot": x_plot,
        "y_pred": y_pred,
        "label": equation,
        "lr": learning_rate,
        "epoch": epoch,
        "x_mean": x_mean
    })

for i, run in enumerate(st.session_state.history):
    if i > 0:
        st.markdown("---")  # 구분선 추가
    st.write(f"### 🔍 예측 {i+1}")
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
    st.markdown(f"""
    #### ✅ <span style='color:#00C851'>예측이 완료되었습니다!</span>  
    🖋️ **수식**: {run['label']}  
    📘 **학습률**: {run['lr']}  
    🔁 **반복 횟수**: {run['epoch']}
    """, unsafe_allow_html=True)
# 🔄 예측 결과 초기화 버튼
# ✅ 초기화 버튼 (항상 보이도록)
col1, col2 = st.columns([7, 3])
with col2:
    if st.button("❌ 모든 예측 결과 삭제"):
        st.session_state.history = []
        st.session_state.selected_model_indices = []
        st.success("✅ 모든 예측 결과가 초기화되었습니다.")
        st.rerun()



# 체크박스 상태 초기화
if "selected_model_indices" not in st.session_state:
    st.session_state.selected_model_indices = []

# 전체 선택 토글 관리
if "select_all_active" not in st.session_state:
    st.session_state.select_all_active = False

if st.session_state.history:
    st.markdown("## 📌 다음 단계로 보내기")

    # 🔘 전체 선택 토글 (눌렀을 때 상태 전환)
    if st.button("☑️ 전체 선택 / 전체 해제"):
        st.session_state.select_all_active = not st.session_state.select_all_active
        if st.session_state.select_all_active:
            # 전체 선택
            st.session_state.selected_model_indices = list(range(len(st.session_state.history)))
        else:
            # 전체 해제
            st.session_state.selected_model_indices = []
        st.rerun()  # 즉시 반영

    # ✅ 체크박스 리스트 출력
    selected = []
    for i, run in enumerate(st.session_state.history):
        label = f"예측 {i+1}: {run['label']}"
        default_checked = i in st.session_state.selected_model_indices
        checked = st.checkbox(label, value=default_checked, key=f"check_{i}")
        if checked:
            selected.append(i)

    # 선택 상태 업데이트
    st.session_state.selected_model_indices = selected

    if st.button("➡️ 다음 단계로 이동"):
        if selected:
            st.switch_page("pages/4_5️⃣_예측입력.py")
        else:
            st.warning("⚠️ 예측선을 하나 이상 선택해야 다음 단계로 이동할 수 있어요.")

