import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import numpy as np
import os

# ✅ 한글 폰트 설정
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    matplotlib.font_manager.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams["font.family"] = font_prop.get_name()
else:
    if platform.system() == "Darwin":
        matplotlib.rcParams["font.family"] = "AppleGothic"
    elif platform.system() == "Windows":
        matplotlib.rcParams["font.family"] = "Malgun Gothic"
    else:
        matplotlib.rcParams["font.family"] = "DejaVu Sans"
    font_prop = None

matplotlib.rcParams["axes.unicode_minus"] = False

st.set_page_config(
    page_title="데이터분석 (4) 예측 실행",
    page_icon="📕",
    layout="centered"
)

# 🔒 자동 생성된 사이드바 메뉴 숨기기
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)


st.title("📕 (4) 예측 실행")
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


# 포함 검사
if "x_values" not in st.session_state or "y_values" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

x_raw = st.session_state.x_values
y_raw = st.session_state.y_values
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# 예측 파라미터 선택
func_type = st.radio("🔢 함수 형태를 선택하세요:", ["1차 함수", "2차 함수"])
learning_rate = st.selectbox("📘 학습률을 선택하세요:", [0.0001, 0.001, 0.01, 0.1])
epoch = st.selectbox("🔁 반복 횟수를 선택하세요:", [100, 500, 1000, 5000, 10000])

if "history" not in st.session_state:
    st.session_state.history = []

# 경사하강법 정의
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
    x_plot = np.linspace(x.min(), x.max(), 100)

    if func_type == "1차 함수":
        x_mean = x.mean()
        x_centered = x - x_mean
        x_input = x_plot - x_mean
        m, b = gradient_descent_linear(x_centered, y, learning_rate, epoch)
        y_pred = m * x_input + b
        m_real = m
        b_real = b - m * x_mean
        equation = f"y = {m_real:.4f}x {'+' if b_real >= 0 else '-'} {abs(b_real):.4f}"
    else:
        x_mean = x.mean()
        x_std = x.std()
        x_scaled = (x - x_mean) / x_std
        x_input_scaled = (x_plot - x_mean) / x_std

        a, b, c = gradient_descent_quadratic(x_scaled, y, learning_rate, epoch)
        y_pred = a * x_input_scaled**2 + b * x_input_scaled + c

        # 정규화된 계수를 원래 X 값 기준으로 변환
        a_real = a / (x_std**2)
        b_real = (-2 * a * x_mean / (x_std**2)) + (b / x_std)
        c_real = (a * x_mean**2 / (x_std**2)) - (b * x_mean / x_std) + c

        equation = (
            f"y = {a_real:.4f}x² "
            f"{'+' if b_real >= 0 else '-'} {abs(b_real):.4f}x "
            f"{'+' if c_real >= 0 else '-'} {abs(c_real):.4f}"
        )

    if np.any(np.isnan(y_pred)) or np.any(np.isinf(y_pred)):
        st.error("❌ 예측 동안 오류가 발생했습니다. 학습률을 낮추거나 반복 횟수를 줄여보세요.")
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
        st.markdown("---")
    st.write(f"### 🔍 예측 {i+1}")
    fig, ax = plt.subplots()
    ax.scatter(x_raw, y_raw, color="blue", label="입력 데이터")
    ax.plot(run["x_plot"], run["y_pred"], color="red", label="예측선")

    if font_prop:
        ax.set_title(f"예측 결과 {i+1}", fontproperties=font_prop)
        ax.set_xlabel(x_label, fontproperties=font_prop)
        ax.set_ylabel(y_label, fontproperties=font_prop)
        ax.legend(prop=font_prop)
    else:
        ax.set_title(f"예측 결과 {i+1}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
    if all(float(x).is_integer() for x in x_raw):
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    else:
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    #### ✅ <span style='color:#00C851'>예측이 완료되었습니다!</span>  
    🖋️ **수식**: {run['label']}  
    📘 **학습률**: {run['lr']}  
    🔁 **반복 횟수**: {run['epoch']}
    """, unsafe_allow_html=True)

    # ✅ 예측 수식 기반 입력값 계산창 추가(수정 예정)
    with st.expander(f"🔍 예측 {i+1}의 수식으로 값을 예측해봅시다."):
        input_x = st.number_input(f"{x_label} 값을 입력하세요 (예: 연도)", value=int(x_raw[-1]) + 1, step=1, key=f"input_{i}")

        try:
            eq = run['label'].replace("y = ", "").replace(" ", "")
            eq = eq.replace("-", "+-").replace("x²", "x^2")
            terms = eq.split("+")
            a_val = b_val = c_val = 0.0
            for term in terms:
                if "x^2" in term:
                    a_val = float(term.replace("x^2", ""))
                elif "x" in term:
                    b_val = float(term.replace("x", ""))
                elif term:
                    c_val = float(term)

            y_input_pred = a_val * input_x**2 + b_val * input_x + c_val
            st.success(f"📌 예측값: {y_input_pred:,.0f}")
        except Exception as e:
            st.warning(f"⚠️ 수식을 해석할 수 없습니다: {e}")



col1, col2 = st.columns([7, 3])
with col2:
    if st.button("❌ 모든 예측 결과 삭제"):
        st.session_state.history = []
        st.session_state.selected_model_indices = []
        st.success("✅ 모든 예측 결과가 초기화되었습니다.")
        st.rerun()

if "selected_model_indices" not in st.session_state:
    st.session_state.selected_model_indices = []

if "select_all_active" not in st.session_state:
    st.session_state.select_all_active = False

if st.session_state.history:
    st.markdown("## 📌 다음 단계로 보내기")
    st.info("예측 모델을 1가지 이상 선택하고 [➡️ 다음] 버튼을 누르세요!")
    if st.button("☑️ 전체 선택 / 전체 해제"):
        st.session_state.select_all_active = not st.session_state.select_all_active
        if st.session_state.select_all_active:
            st.session_state.selected_model_indices = list(range(len(st.session_state.history)))
        else:
            st.session_state.selected_model_indices = []
        st.rerun()

    selected = []
    for i, run in enumerate(st.session_state.history):
        label = f"예측 {i+1}: {run['label']}"
        default_checked = i in st.session_state.selected_model_indices
        checked = st.checkbox(label, value=default_checked, key=f"check_{i}")
        if checked:
            selected.append(i)

    st.session_state.selected_model_indices = selected

    colA, colB, colC = st.columns([3, 15, 3])
    with colA:
        if st.button("⬅️ 이전"):
            st.switch_page("pages/8_📕_데이터분석_(3)_데이터입력.py")
    with colC:
        if st.button("➡️ 다음"):
            if selected:
                st.switch_page("pages/10_📕_데이터분석_(5)_예측해석.py")
            else:
                st.warning("⚠️ 예측선을 하나 이상 선택해야 다음 단계로 이동할 수 있어요.")