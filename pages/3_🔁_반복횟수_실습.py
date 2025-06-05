import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------------- 데이터 및 설정 ----------------
np.random.seed(42)
x = np.linspace(1, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 1, size=len(x))

x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_plot = x_input - x_mean

fixed_learning_rate = 0.001  # 학습률 고정
epoch_options = [100, 500, 1000, 5000]

# 경사하강법 함수
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
if "draw_graph_epochs" not in st.session_state:
    st.session_state.draw_graph_epochs = False
if "select_action_epochs" not in st.session_state:
    st.session_state.select_action_epochs = None
for ep in epoch_options:
    key = f"epoch_checkbox_{ep}"
    if key not in st.session_state:
        st.session_state[key] = (ep == 100)

# ---------------- 버튼 작업 처리 ----------------
if st.session_state.select_action_epochs == "select_all":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = True
    st.session_state.select_action_epochs = None
    st.rerun()

elif st.session_state.select_action_epochs == "clear_all":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = False
    st.session_state.select_action_epochs = None
    st.rerun()

elif st.session_state.select_action_epochs == "reset":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = (ep == 100)
    st.session_state.draw_graph_epochs = False
    st.session_state.select_action_epochs = None
    st.rerun()

# ---------------- UI 구성 ----------------
st.markdown("## 🔁 반복횟수 실습")
st.markdown(f"학습률 **{fixed_learning_rate}** 를 고정하고 반복횟수에 따라 예측 결과가 어떻게 달라지는지 비교해보세요.")

# 체크박스 선택
st.markdown("### ✅ 비교하고 싶은 반복횟수를 선택하세요:")
cols = st.columns(len(epoch_options))
selected_epochs = []
for i, ep in enumerate(epoch_options):
    key = f"epoch_checkbox_{ep}"
    if cols[i].checkbox(f"{ep}", key=key):
        selected_epochs.append(ep)

# 버튼 영역
btn_row = st.columns([2, 1, 1, 1])
with btn_row[0]:
    if st.button("📈 선택한 반복횟수로 그래프 그리기", use_container_width=True):
        if selected_epochs:
            st.session_state.draw_graph_epochs = True
            st.session_state.selected_epochs_snapshot = selected_epochs.copy()
        else:
            st.warning("반복횟수를 하나 이상 선택해주세요.")
            st.session_state.draw_graph_epochs = False
with btn_row[1]:
    if st.button("✅ 전체 선택", use_container_width=True):
        st.session_state.select_action_epochs = "select_all"
        st.rerun()
with btn_row[2]:
    if st.button("❎ 전체 해제", use_container_width=True):
        st.session_state.select_action_epochs = "clear_all"
        st.rerun()
with btn_row[3]:
    if st.button("♻️ 초기화", use_container_width=True):
        st.session_state.select_action_epochs = "reset"
        st.rerun()

# ---------------- 결과 출력 ----------------
if st.session_state.draw_graph_epochs and "selected_epochs_snapshot" in st.session_state:
    st.markdown("### 📊 반복횟수별 그래프 비교")
    tabs = st.tabs([f"반복={ep}" for ep in st.session_state.selected_epochs_snapshot])
    for i, ep in enumerate(st.session_state.selected_epochs_snapshot):
        with tabs[i]:
            m, b = gradient_descent(x_centered, y, fixed_learning_rate, ep)
            y_pred = m * x_input + b

            fig, ax = plt.subplots()
            ax.scatter(x, y, color="blue", label="입력 데이터")
            ax.plot(x_plot + x_mean, y_pred, color="red", label=f"예측선 (반복={ep})")
            ax.set_title(f"반복횟수 {ep}회에 대한 예측 결과")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            st.pyplot(fig)

# ---------------- 정리 영역 ----------------
st.markdown("### 📘 실습을 통해 무엇을 배웠나요?")
st.text_area(
    "여러 반복횟수를 비교한 결과, 어떤 점을 배웠나요? 반복이 많아질수록 어떤 변화가 있었나요?",
    height=150,
    placeholder="예: 반복횟수가 늘어날수록 예측선이 점점 더 정확하게 수렴하는 것을 볼 수 있었습니다.",
    key="epoch_summary"
)
