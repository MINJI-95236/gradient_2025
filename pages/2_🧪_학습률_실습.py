import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':  # Windows
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux (예: Ubuntu 등)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지



# ---------------- 데이터 및 함수 정의 ----------------
np.random.seed(42)
x = np.linspace(1, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 1, size=len(x))

x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_plot = x_input - x_mean
fixed_epochs = 100

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

# ---------------- 상태 초기화 ----------------
learning_rates = [0.0001, 0.001, 0.01, 0.1]

if "draw_graph" not in st.session_state:
    st.session_state.draw_graph = False
if "select_action" not in st.session_state:
    st.session_state.select_action = None
for lr in learning_rates:
    key = f"lr_checkbox_{lr}"
    if key not in st.session_state:
        st.session_state[key] = (lr == 0.001)

# ---------------- 버튼 작업 처리 (선택/초기화 등) ----------------
if st.session_state.select_action == "select_all":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = True
    st.session_state.select_action = None
    st.rerun()

elif st.session_state.select_action == "clear_all":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = False
    st.session_state.select_action = None
    st.rerun()

elif st.session_state.select_action == "reset":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = (lr == 0.001)
    st.session_state.draw_graph = False
    st.session_state.select_action = None
    st.rerun()

# ---------------- UI 구성 시작 ----------------
st.markdown("## 🔍 학습률 실습")

# 학습률 체크박스
st.markdown("### ✅ 비교하고 싶은 학습률을 선택하세요:")
cols = st.columns(len(learning_rates))
selected_rates = []
for i, lr in enumerate(learning_rates):
    key = f"lr_checkbox_{lr}"
    if cols[i].checkbox(f"{lr}", key=key):
        selected_rates.append(lr)

current_selected = selected_rates.copy()

st.markdown("")

# 실행 및 제어 버튼 한 줄 구성
btn_row = st.columns([2, 1, 1, 1])
with btn_row[0]:
    if st.button("📈 선택한 학습률로 그래프 그리기", use_container_width=True):
        if selected_rates:
            st.session_state.draw_graph = True
            st.session_state.selected_rates_snapshot = selected_rates.copy()  # ✅ 선택 상태 저장
        else:
            st.warning("학습률을 하나 이상 선택해주세요.")
            st.session_state.draw_graph = False
with btn_row[1]:
    if st.button("✅ 전체 선택", use_container_width=True):
        st.session_state.select_action = "select_all"
        st.rerun()
with btn_row[2]:
    if st.button("❎ 전체 해제", use_container_width=True):
        st.session_state.select_action = "clear_all"
        st.rerun()
with btn_row[3]:
    if st.button("♻️ 초기화", use_container_width=True):
        st.session_state.select_action = "reset"
        st.rerun()

# ---------------- 결과 출력 ----------------
if st.session_state.draw_graph and "selected_rates_snapshot" in st.session_state:
    st.markdown("### 📊 학습률별 그래프 비교")
    tabs = st.tabs([f"학습률={lr}" for lr in st.session_state.selected_rates_snapshot])
    for i, lr in enumerate(st.session_state.selected_rates_snapshot):
        with tabs[i]:
            m, b = gradient_descent(x_centered, y, lr, fixed_epochs)
            y_pred = m * x_input + b

            fig, ax = plt.subplots()
            ax.scatter(x, y, color="blue", label="입력 데이터")
            ax.plot(x_plot + x_mean, y_pred, color="red", label=f"예측선 (lr={lr})")
            ax.set_title(f"학습률 {lr} 에 대한 예측 결과")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            st.pyplot(fig)


# ---------------- 실습 정리 ----------------
st.markdown("### 📘 실습을 통해 무엇을 배웠나요?")
st.text_area(
    "여러 학습률을 비교한 결과, 어떤 점을 배웠나요? 가장 적절한 학습률은 무엇이라고 생각하나요?",
    height=150,
    placeholder="예: 학습률 0.001이 가장 안정적으로 수렴함을 확인했습니다. 너무 큰 값은 발산하고, 너무 작은 값은 변화가 거의 없습니다.",
    key="final_summary"
)
