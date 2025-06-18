import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import os
import math

# ✅ 페이지 설정
st.set_page_config(
    page_title="🍧 예제 - Q. 아이스크림을 많이 팔 수 있을까?",
    page_icon="🍧",
    layout="wide"
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
# ✅ 한글 폰트 설정
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name
    font_prop = fm.FontProperties(fname=font_path)
else:
    if platform.system() == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"
    elif platform.system() == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    font_prop = None

plt.rcParams["axes.unicode_minus"] = False

# ✅ 사이드바 메뉴 구성
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
    st.markdown("## 🍧 예제")
    st.page_link("pages/_5_1_example_icecream_prediction.py", label="Q. 아이스크림을 많이 팔 수 있을까?")

    st.markdown("---")
    st.markdown("## 📊 데이터분석")
    st.page_link("pages/6_📕_데이터분석_(1)_기본정보입력.py", label="(1) 기본 정보 입력")
    st.page_link("pages/7_📕_데이터분석_(2)_분석주제선택.py", label="(2) 분석 주제 선택")
    st.page_link("pages/8_📕_데이터분석_(3)_데이터입력.py", label="(3) 데이터 입력")
    st.page_link("pages/9_📕_데이터분석_(4)_예측실행.py", label="(4) 예측 실행")
    st.page_link("pages/10_📕_데이터분석_(5)_예측해석.py", label="(5) 예측 해석")
    st.page_link("pages/11_📕_데이터분석_(6)_요약결과.py", label="(6) 요약 결과")

# ✅ 본문 구성
st.title("🍧 예제 - Q. 아이스크림을 많이 팔 수 있을까?")
st.markdown("""
이 예제에서는 기온과 아이스크림 판매량 간의 관계를 학습하여  
미래의 판매량을 예측할 수 있는 모델을 직접 구성해봅니다.
""")

# 1️⃣ 데이터 입력
st.subheader("1️⃣ 데이터 입력")
st.markdown("기온(℃)과 아이스크림 판매량(개)을 아래 표에 직접 입력하거나 수정해보세요.")

df_default = pd.DataFrame({
    "기온(℃)": [15.0, 15.7, 16.5, 17.2, 17.9, 18.6, 19.3, 20.0, 20.7, 21.4,
              22.1, 22.9, 23.6, 24.3, 25.0, 25.7, 26.4, 27.1, 27.9, 28.6,
              29.3, 30.0, 30.7, 31.4, 32.1, 32.9, 33.6, 34.3, 35.0, 35.7,
              36.4, 37.1, 37.9, 38.6, 39.3],
    "판매량(개)": [107, 108, 116, 124, 119, 123, 125, 136, 130, 143,
                140, 153, 155, 147, 162, 162, 173, 169, 172, 176,
                177, 189, 187, 195, 195, 200, 204, 204, 216, 210,
                222, 228, 224, 225, 232]
})
df_input = st.data_editor(df_default, use_container_width=True, num_rows="dynamic")

# 2️⃣ 산점도
if "scatter_shown" not in st.session_state:
    st.session_state.scatter_shown = False

if st.button("📊 산점도 보기"):
    if df_input.dropna().shape[0] < 2:
        st.warning("입력된 데이터가 충분하지 않습니다. 최소 2개 이상 입력해주세요.")
    else:
        st.session_state.scatter_shown = True

if st.session_state.scatter_shown:
    valid_data = df_input.dropna()
    valid_data = valid_data.sort_values(by="기온(℃)")
    st.subheader("2️⃣ 산점도")
    fig, ax = plt.subplots()
    ax.scatter(valid_data["기온(℃)"], valid_data["판매량(개)"], color='blue')
    ax.set_title("기온과 아이스크림 판매량의 관계")
    ax.set_xlabel("기온(℃)")
    ax.set_ylabel("판매량(개)")
    st.pyplot(fig)

    # ✅ 초기 설정
if "lr_value" not in st.session_state:
    st.session_state.lr_value = 0.0001  # 기본 학습률
if "epochs_value" not in st.session_state:
    st.session_state.epochs_value = 1000  # 기본 반복횟수

# ✅ 학습률 조절
st.subheader("3️⃣ 모델 설정")

# 🔧 학습률 조절 UI - 한 줄 구성
st.markdown("**학습률 (learning rate)**")
lr_col1, lr_col2, lr_col3, lr_col4 = st.columns([1, 5, 1, 4])

with lr_col1:
    if st.button("➖", key="lr_minus"):
        st.session_state.lr_value = max(0.0001, st.session_state.lr_value - 0.0001)

with lr_col2:
    new_lr = st.slider(
    "학습률", 0.0001, 0.0050, st.session_state.lr_value,
    step=0.0002, format="%.4f", label_visibility="collapsed"
)
st.session_state.lr_value = new_lr

with lr_col3:
    if st.button("➕", key="lr_plus"):
        st.session_state.lr_value = min(0.01, st.session_state.lr_value + 0.0001)

with lr_col4:
    st.markdown(
        f"""<div style='margin-top: 6px;'>
        👉 <b>현재 학습률: {st.session_state.lr_value:.4f}</b><br>
        <span style='font-size: 12px; color: gray;'>🔍 너무 크면 발산할 수 있어요</span>
        </div>""", unsafe_allow_html=True
    )

# 🔧 반복횟수 조절 UI - 한 줄 구성
st.markdown("**반복 횟수 (epochs)**")
ep_col1, ep_col2, ep_col3, ep_col4 = st.columns([1, 5, 1, 4])

with ep_col1:
    if st.button("➖", key="ep_minus"):
        st.session_state.epochs_value = max(100, st.session_state.epochs_value - 100)

with ep_col2:
    new_epochs = st.slider(
        "반복 횟수", 100, 5000, st.session_state.epochs_value,
        step=100, label_visibility="collapsed"
    )
    st.session_state.epochs_value = new_epochs

with ep_col3:
    if st.button("➕", key="ep_plus"):
        st.session_state.epochs_value = min(5000, st.session_state.epochs_value + 100)

with ep_col4:
    st.markdown(
    f"""<div style='margin-top: 6px;'>
    👉 <b>현재 반복 횟수: {st.session_state.epochs_value}회</b><br>
    <span style='font-size: 12px; color: gray;'>📈 충분한 반복은 정확도를 높일 수 있어요</span>
    </div>""", unsafe_allow_html=True
)

# ✅ 슬라이더 변경 감지 후 예측 플래그 해제
if "prev_lr" not in st.session_state:
    st.session_state.prev_lr = st.session_state.lr_value
if "prev_epochs" not in st.session_state:
    st.session_state.prev_epochs = st.session_state.epochs_value

if st.session_state.lr_value != st.session_state.prev_lr:
    st.session_state.prev_lr = st.session_state.lr_value
if st.session_state.epochs_value != st.session_state.prev_epochs:
    st.session_state.prev_epochs = st.session_state.epochs_value



# ✅ 최종 사용 변수
lr = st.session_state.lr_value
epochs = st.session_state.epochs_value


# ⛳ 경사하강법 함수
def train_model(X, y, lr, epochs):
    m = 0
    b = 0
    n = len(X)
    for _ in range(epochs):
        y_pred = m * X + b
        error = y_pred - y
        m_grad = (2/n) * np.dot(error, X)
        b_grad = (2/n) * error.sum()
        m -= lr * m_grad
        b -= lr * b_grad
    return m, b

# 예측 실행 버튼
if st.button("📈 예측 그래프 그리기"):
    st.session_state.predict_requested = True
    if "input_temp" not in st.session_state:
        st.session_state.input_temp = 25

# 최초 상태 설정
if "input_temp" not in st.session_state:
    st.session_state.input_temp = 25
if "predict_requested" not in st.session_state:
    st.session_state.predict_requested = False

# 예측 그래프 및 슬라이더 유지 출력
if st.session_state.predict_requested:
    try:
        valid_data = df_input.copy()
        valid_data["기온(℃)"] = pd.to_numeric(valid_data["기온(℃)"], errors="coerce")
        valid_data["판매량(개)"] = pd.to_numeric(valid_data["판매량(개)"], errors="coerce")
        valid_data = valid_data.dropna()

        X = valid_data["기온(℃)"].values
        y = valid_data["판매량(개)"].values
        m, b = train_model(X, y, lr, epochs)
        y_pred = m * X + b

        # 발산 여부 체크
        if any([math.isnan(m), math.isnan(b), np.any(np.isnan(y_pred)), np.any(np.isinf(y_pred))]):
            st.error("⚠️ 학습률이 너무 크거나 반복 횟수가 너무 많아 예측이 발산했습니다.")
            st.stop()

        # 정확도 계산
        ss_total = np.sum((y - y.mean()) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r2 = 1 - ss_res / ss_total
        accuracy = round(r2 * 100, 2)

        # 결과 출력
        st.subheader("4️⃣ 예측 결과")
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.scatter(X, y, color='blue', label='실제값')
            sorted_idx = X.argsort()
            ax.plot(X[sorted_idx], y_pred[sorted_idx], color='red', label='예측값')
            ax.set_xlabel("기온(℃)")
            ax.set_ylabel("판매량(개)")
            ax.legend()
            ax.set_title("예측 결과")
            st.pyplot(fig)

        with col2:
            st.markdown("#### 📌 예측 수식")
            st.latex(f"y = {m:.2f} \\times x + {b:.2f}")
            st.markdown(f"**반복 횟수**: {epochs}회")
            st.markdown(f"**학습률**: {lr}")
            st.markdown(f"**정확도**: {accuracy}%")

            # 🔁 슬라이더는 계속 유지되며 값만 갱신됨
            input_temp = st.slider("예측하고 싶은 기온(℃)", 15, 40, value=st.session_state.input_temp)
            st.session_state.input_temp = input_temp
            pred = m * input_temp + b
            st.markdown(f"🌡️ 기온이 **{input_temp}℃**일 때, 판매량은 **{pred:.0f}개**입니다.")
    except Exception as e:
        st.error(f"예측에 실패했습니다: {e}")
