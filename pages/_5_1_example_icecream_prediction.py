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
    page_title="예제 - Q. 나 혼자 산다! 다 혼자 산다?",
    page_icon="🏠",
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

# ✅ 본문 구성
st.title("🏠 나 혼자 산다! 다 혼자 산다?")

# 그림 + 설명 (데이터 입력 섹션 위)

col1, col2 = st.columns([2, 3])  # 왼쪽: 영상 / 오른쪽: 설명

with col1:
    st.image("images/1인가구메인그림.png", use_container_width=True)


with col2:
    st.markdown("""
    ### 📽️ 1인 가구, 얼마나 늘어날까?

    우리 주변에서 1인 가구가 점점 많아지고 있다는 이야기를 많이 들어봤을 거예요.  
    그런데 정말로 얼마나 늘어났고, 앞으로 얼마나 더 늘어날까요?

    이 영상에서는 실제 데이터를 바탕으로  
    **연도별 1인 가구 비율이 어떻게 변화해왔는지**를 확인하고,  
    이를 바탕으로 **미래의 비율을 예측하는 과정**을 보여줍니다.

    아래 표에 있는 데이터를 직접 수정하거나 새로운 값을 추가하면서,  
    우리만의 예측 모델을 만들어볼 수 있어요!
    """)


st.markdown("---")

# 1️⃣ 데이터 입력
st.subheader("1️⃣ 데이터 입력")
st.markdown("연도와 1인 가구 비율(%)을 아래 표에 직접 입력하거나 수정해보세요.")

df_default = pd.DataFrame({
    "연도": [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015,
           2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "1인 가구 비율(%)": [4.8, 6.9, 9, 12.7, 15.5, 20, 23.9, 27.2,
                  27.9, 28.6, 29.3, 30.2, 31.7, 33.4, 34.5, 35.5]
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
    valid_data = valid_data.sort_values(by="연도")
    st.subheader("2️⃣ 산점도")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(valid_data["연도"], valid_data["1인 가구 비율(%)"], color='blue')
    ax.set_title("연도와 1인 가구 비율의 관계")
    ax.set_xlabel("연도")
    ax.set_ylabel("1인 가구 비율(%)")
    st.pyplot(fig, use_container_width=False)

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
        st.session_state.input_temp = 2024

# 최초 상태 설정
if "input_temp" not in st.session_state:
    st.session_state.input_temp = 2024
if "prev_input_temp" not in st.session_state:
    st.session_state.prev_input_temp = 2024
if "predict_requested" not in st.session_state:
    st.session_state.predict_requested = False

# 예측 그래프 및 슬라이더 유지 출력
if st.session_state.predict_requested or (
    st.session_state.input_temp != st.session_state.prev_input_temp
):
    try:
        valid_data = df_input.copy()
        valid_data["연도"] = pd.to_numeric(valid_data["연도"], errors="coerce")
        valid_data["1인 가구 비율(%)"] = pd.to_numeric(valid_data["1인 가구 비율(%)"], errors="coerce")
        valid_data = valid_data.dropna()

        X = valid_data["연도"].values
        X_mean = X.mean()  # 중심화 기준
        X_scaled = X - X_mean
        y = valid_data["1인 가구 비율(%)"].values
        m, b = train_model(X_scaled, y, lr, epochs)
        y_pred = m * X_scaled + b

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
            ax.set_xlabel("연도")
            ax.set_ylabel("1인 가구 비율(%)")
            ax.legend()
            ax.set_title("예측 결과")
            st.pyplot(fig)

        with col2:
            st.markdown("#### 📌 예측 수식")
            # 수식에서 사용할 계수 (정규화된 모델에서 원래 x로 복원한 것)
            true_m = m
            true_b = b - m * X_mean

            # 이 수식을 화면에 표시
            st.latex(f"y = {true_m:.4f} \\times x {'+' if true_b >= 0 else '-'} {abs(true_b):.2f}")


            st.markdown(f"**반복 횟수**: {epochs}회")
            st.markdown(f"**학습률**: {lr}")

            # 🔁 슬라이더는 계속 유지되며 값만 갱신됨
            input_temp = st.number_input(
                label="예측하고 싶은 연도(예:2026)를 입력하세요",
                min_value=1980,
                max_value=2100,
                value=int(st.session_state.input_temp),
                step=1, 
                format="%d"
            )
            if input_temp != st.session_state.input_temp:
                st.session_state.input_temp = input_temp
                st.rerun()
                        # 1️⃣ 먼저 이전 값을 백업
            st.session_state.prev_input_temp = st.session_state.input_temp

            # 2️⃣ 그 다음에 새 값을 입력
            st.session_state.input_temp = input_temp
            input_scaled = input_temp - X_mean
            pred = true_m * input_temp + true_b

            st.markdown(f"📅 연도가 **{input_temp}년**일 때, 1인 가구 비율은 **{pred:.1f}%**입니다.")

            accuracy_color = "red" if accuracy >= 90 else "gray"
            accuracy_weight = "bold" if accuracy >= 90 else "normal"

            st.markdown(
                f"""
                <div style='text-align: center; font-size: 32px; font-weight: {accuracy_weight}; color: {accuracy_color};'>
                    🎯 모델 정확도: {accuracy:.2f}%</div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"예측에 실패했습니다: {e}")

    st.markdown("### 🔍 당신의 분석을 선택해보세요!")

    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("📈 1인 가구는 점점 증가합니다.", key="increase"):
            st.success("✅ 훌륭해요! 실제 데이터에서도 꾸준히 증가하는 추세가 나타납니다.")
            st.markdown("""
            <div style="background-color:#e0f7fa; padding:15px; border-radius:10px; border-left:6px solid #00acc1;">
            <b>📌 보충 설명:</b>  
            1인 가구 비율은 1980년 4.8%에서 2023년 35.5%까지 꾸준히 증가했어요.  
            이는 고령화, 비혼 인구 증가, 개인의 독립적 삶 선호 등 다양한 사회적 요인과 관련되어 있어요.  
            미래에는 더 많은 혼자 사는 사람들이 생겨날 가능성이 높습니다.
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        if st.button("📉 1인 가구는 점점 감소합니다.", key="decrease"):
            st.error("❌ 다시 생각해봐요! 그래프를 보면 1인 가구 비율은 점점 증가하고 있어요.")
            st.markdown("""
            <div style="background-color:#fff3e0; padding:15px; border-radius:10px; border-left:6px solid #ffb74d;">
            <b>📌 확인해볼 점:</b>  
            그래프를 다시 한 번 살펴보세요.  
            연도에 따라 1인 가구 비율이 거의 꾸준히 상승하고 있다는 점이 보일 거예요.  
            사회 변화에 따라 이러한 추세는 당분간 계속될 것으로 예상됩니다.
            </div>
            """, unsafe_allow_html=True)
