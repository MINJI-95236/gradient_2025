import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter, FormatStrFormatter
import platform
import matplotlib.font_manager as fm
import matplotlib
import os

st.set_page_config(
    page_title="데이터분석 (6) 요약 결과",
    page_icon="📕",
    layout="wide"
)

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

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
        }

        [data-testid="stVerticalBlock"] {
            overflow: visible !important;
        }

        .stButton button {
            margin-top: 12px;
        }

        /* ✅ 페이지 인쇄 시 최적화 설정 */
        @media print {
            html, body {
                height: auto !important;
                overflow: visible !important;
                margin: 0 !important;
                padding: 0 !important;
                zoom: 85%;  /* ✅ 한 페이지에 맞추기 위한 축소 */
            }

            .element-container {
                page-break-inside: avoid;
                break-inside: avoid;
            }

            .stButton, .stSidebar {
                display: none !important;  /* 버튼, 사이드바 숨김 */
            }

            .main {
                padding: 0 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# 🔒 자동 생성된 사이드바 메뉴 숨기기
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)
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

st.title("📕 (6) 요약 결과")

# 1️⃣ 기본 정보 섹션
with st.container():
    info_data = {
        "이름": st.session_state.get("name", "정보 없음"),
        "학번": st.session_state.get("student_id", "정보 없음"),
        "학교": st.session_state.get("school", "정보 없음"),
        "날짜": st.session_state.get("date", "정보 없음")
    }
    cols = st.columns(4)
    for i, (label, value) in enumerate(info_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background-color: #f3f4f6; padding: 12px 15px; border-radius: 8px;
                        font-size: 15px; color: #1f2937;'>
                <div style='font-weight: 700; font-size: 16px;'>{label}</div>
                <div style='margin-top: 5px; font-size: 15px;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

# 2️⃣ 분석 주제
with st.container():
    st.markdown("### 🔵 선택한 분석 주제")
    subject = st.session_state.get('subject', '정보 없음')
    st.markdown(f"""
    <div style='background-color: #f3f4f6; color: #111827;
                padding: 15px 20px; border-radius: 10px;
                font-size: 17px; margin-top: 8px; margin-bottom: 0px;'>
        \U0001F4CC <strong>주제:</strong> {subject}
    </div>
    """, unsafe_allow_html=True)

# 3️⃣ 입력한 데이터 및 분석
with st.container():
    st.markdown("### 🟣 입력한 데이터 및 분석")

    if 'table_data' in st.session_state:
        st.markdown("#### \U0001F4CA 입력한 데이터")
        display_df = st.session_state.table_data.rename(columns={
            "x": st.session_state.get("x_label", "x"),
            "y": st.session_state.get("y_label", "y")
        })
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("입력된 데이터가 없습니다.")

    if 'x_values' in st.session_state and 'y_values' in st.session_state:
        st.markdown("#### \U0001F4C8 산점도 그래프")
        fig, ax = plt.subplots(figsize=(6, 4)) 
        ax.scatter(st.session_state.x_values, st.session_state.y_values, color='blue')
        if font_prop:
            ax.set_xlabel(st.session_state.get("x_label", "x"), fontproperties=font_prop)
            ax.set_ylabel(st.session_state.get("y_label", "y"), fontproperties=font_prop)
        else:
            ax.set_xlabel(st.session_state.get("x_label", "x"))
            ax.set_ylabel(st.session_state.get("y_label", "y"))
        st.pyplot(fig)
    else:
        st.warning("산점도 데이터를 불러올 수 없습니다.")

    if 'analysis_text' in st.session_state:
        st.markdown(f"""
        <div style='background-color: #f9fafb; padding: 18px 20px; border-radius: 10px;
                    font-size: 16px; line-height: 1.6; color: #111827;
                    border: 1px solid #e5e7eb; margin-top: 20px;'>
            <div style='font-weight: 600; font-size: 18px; margin-bottom: 10px;'>✏️ 분석 내용</div>
            {st.session_state.analysis_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("분석 내용이 없습니다.")

# 5️⃣ 예측 결과 해석
with st.container():
    st.markdown("### 🟡 예측 결과 및 해석")

    if 'history' in st.session_state and 'selected_model_indices' in st.session_state:
        for idx in st.session_state.selected_model_indices:
            model = st.session_state.history[idx]
            with st.expander(f"🔍 모델 {idx + 1} (학습률={model['lr']}, 반복횟수={model['epoch']})"):
                st.markdown(f"**예측 수식:** {model['label']}")

                fig, ax = plt.subplots(figsize=(6, 4)) 
                ax.scatter(st.session_state.x_values, st.session_state.y_values, label="입력 데이터", color="blue")
                ax.plot(model["x_plot"], model["y_pred"], label="예측 선", color="red")
                if font_prop:
                    ax.set_xlabel(st.session_state.get("x_label", "x"), fontproperties=font_prop)
                    ax.set_ylabel(st.session_state.get("y_label", "y"), fontproperties=font_prop)
                else:
                    ax.set_xlabel(st.session_state.get("x_label", "x"))
                    ax.set_ylabel(st.session_state.get("y_label", "y"))
                ax.legend()
                st.pyplot(fig)

                reflection = st.session_state.get(f"reflection_{idx}", "해석 내용 없음")
                st.markdown(f"""
                <div style='background-color: #f3f4f6; padding: 15px 20px; border-radius: 10px;
                            font-size: 16px; color: #111827; margin-top: 20px; margin-bottom: 30px;'>
                    <strong>✏️ 예측 해석</strong><br><br>
                    {reflection}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("예측 결과 정보가 부족하거나 선택된 모델이 없습니다.")

st.markdown("""
    <style>
        @media print {
            .no-print { display: none !important; }
        }
    </style>
    <div class="no-print" style="margin-top: 40px; display: flex; justify-content: flex-start;">
        <form>
            <input type="submit" value="📄 PDF로 저장하기" formaction="javascript:window.print()" style="
                background-color: #93c5fd;
                color: black;
                padding: 12px 24px;
                font-size: 16px;
                border: 1px solid #111;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
                font-weight: bold;
            ">
        </form>
    </div>
""", unsafe_allow_html=True)
