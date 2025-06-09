import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter, FormatStrFormatter
import platform
import matplotlib.font_manager as fm
import matplotlib
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

st.set_page_config(page_title="요약 결과", layout="wide")
st.title("\U0001F4D8 최종 요약 결과")

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
    st.markdown("### \U0001F537 선택한 분석 주제")
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
    st.markdown("### \U0001F7E2 입력한 데이터 및 분석")

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
        fig, ax = plt.subplots()
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
    st.subheader("5️⃣ 예측 결과 및 해석")

    if 'history' in st.session_state and 'selected_model_indices' in st.session_state:
        for idx in st.session_state.selected_model_indices:
            model = st.session_state.history[idx]
            with st.expander(f"🔍 모델 {idx + 1} (학습률={model['lr']}, 반복횟수={model['epoch']})"):
                st.markdown(f"**예측 수식:** `{model['label']}`")

                fig, ax = plt.subplots()
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

# 📄 PDF 저장 안내
if "show_pdf_guide" not in st.session_state:
    st.session_state.show_pdf_guide = False

if st.button("📄 PDF 저장 안내 보기"):
    st.session_state.show_pdf_guide = not st.session_state.show_pdf_guide

if st.session_state.show_pdf_guide:
    st.markdown("""
    <div style='background-color: #fef9c3; padding: 20px; border-radius: 12px;
                font-size: 16px; color: #111827; border: 1px solid #fcd34d;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                margin-top: 10px; transition: all 0.3s ease;'>
        <h4 style='margin-top: 0;'>📄 요약 결과를 PDF로 저장하는 방법</h4>
        <ol>
            <li><strong>Ctrl + P</strong> 또는 <strong>⌘ + P</strong>를 누르세요</li>
            <li>프린터에서 <strong>PDF로 저장</strong>을 선택하세요</li>
            <li><em>여백 없음</em>, <em>배경 그래픽 포함</em>을 설정하면 더 보기 좋습니다</li>
            <li><strong>저장</strong> 버튼을 눌러 완료!</li>
        </ol>
        <p style='margin-top: 10px;'>🔍 <strong>TIP:</strong> 예측 결과는 <em>열어둔 상태</em>로 저장하는 걸 추천해요!</p>
    </div>
    """, unsafe_allow_html=True)
