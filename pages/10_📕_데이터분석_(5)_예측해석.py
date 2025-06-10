import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter, FormatStrFormatter
import platform
import matplotlib.font_manager as fm
import matplotlib
from fpdf import FPDF
import io
import tempfile
from PIL import Image
import os

# ✅ 폰트 설정
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
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
    page_title="📕 데이터분석 (5) 예측 해석",
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

st.title("📕 (5) 예측 해석")

# 🔒 이전 단계 데이터 확인
if "selected_model_indices" not in st.session_state or "history" not in st.session_state:
    st.warning("먼저 4단계에서 예측을 실행하고 선택해주세요!")
    st.stop()

x_raw = st.session_state.x_values
y_raw = st.session_state.y_values
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# 🔁 선택된 예측선들에 대해 반복
for idx in st.session_state.selected_model_indices:
    run = st.session_state.history[idx]

    st.markdown(f"### 🔍 선택한 예측 {idx+1}")

    # 📊 그래프 출력
    fig, ax = plt.subplots()
    ax.scatter(x_raw, y_raw, color="blue", label="입력 데이터")
    ax.plot(run["x_plot"], run["y_pred"], color="red", label="예측선")
    if font_prop:
        ax.set_xlabel(x_label, fontproperties=font_prop)
        ax.set_ylabel(y_label, fontproperties=font_prop)
        ax.set_title(f"예측 결과 {idx+1}", fontproperties=font_prop)
        ax.legend(prop=font_prop)
    else:
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"예측 결과 {idx+1}")
        ax.legend()
    ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
    if all(float(x).is_integer() for x in x_raw):
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    else:
        ax.xaxis.set_major_formatter(ScalarFormatter())
    st.pyplot(fig)

    # ℹ️ 수식 및 정보 출력
    st.markdown(
        f"""
        📌 **수식**: {run['label']}  
        📘 **학습률**: {run['lr']}  
        🔁 **반복 횟수**: {run['epoch']}
        """
    )

    # 📝 학생 입력 칸
    # 반복 안에서 명시적으로 저장
    value = st.text_area(
        f"🧠 예측 {idx+1} 해석 입력",
        value=st.session_state.get(f"reflection_{idx}", ""),
        placeholder="이 예측선은 어떤 의미를 가질까요? 예측 결과를 해석해봅시다.",
        key=f"text_area_{idx}"  # 키는 UI용으로 별도로 둡니다
        )
    st.session_state[f"reflection_{idx}"] = value



st.success("✅ 예측 결과에 대한 해석을 모두 마쳤습니다!")

st.markdown("---")
st.subheader("📘 최종 요약 페이지로 이동")

if st.button("➡️ 최종 요약 보기"):
    # ✅ 해석 내용 강제 저장 (빈 문자열도 기본값 설정)
    for idx in st.session_state.selected_model_indices:
        key = f"reflection_{idx}"
        value = st.session_state.get(key, "").strip()
        if not value:
            st.session_state[key] = "해석이 작성되지 않았습니다."

    st.switch_page("pages/11_📕_데이터분석_(6)_요약결과.py")


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
