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

# ✅ 한글 폰트 설정
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

st.title("✏️ 5단계: 예측 결과 해석하기")

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
        ✅ 예측이 완료되었습니다!  
        📌 **수식**: {run['label']}  
        📘 **학습률**: {run['lr']}  
        🔁 **반복 횟수**: {run['epoch']}
        """
    )

    # 📝 학생 입력 칸
    st.text_area(
        f"🧠 예측 {idx+1} 해석 입력",
        placeholder="이 예측선은 어떤 의미를 가질까요? 예측 결과를 해석해봅시다.",
        key=f"reflection_{idx}"
    )

# 📄 PDF 저장 버튼
if st.button("📄 PDF로 저장"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('NotoSans', '', 'fonts/NotoSansKR-Regular.ttf', uni=True)
    pdf.set_font('NotoSans', size=14)

    pdf.cell(200, 10, txt="📘 나의 AI 예측 학습지", ln=True)
    pdf.set_font('NotoSans', size=12)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"이름: {st.session_state.get('name', '')}  학번: {st.session_state.get('student_id', '')}", ln=True)
    pdf.cell(200, 10, txt=f"학교: {st.session_state.get('school', '')}  날짜: {st.session_state.get('date', '')}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"🔍 분석 주제: {st.session_state.get('subject', '')}")

    for i, idx in enumerate(st.session_state.selected_model_indices):
        run = st.session_state.history[idx]
        pdf.ln(5)
        pdf.set_font('NotoSans', size=12)
        pdf.cell(200, 10, txt=f"예측 {i+1} 수식:", ln=True)
        pdf.multi_cell(0, 10, txt=f"{run['label']}")
        pdf.cell(200, 10, txt=f"학습률: {run['lr']} / 반복횟수: {run['epoch']}", ln=True)
        reflection = st.session_state.get(f"reflection_{idx}", "(미작성)")
        pdf.multi_cell(0, 10, txt=f"📝 해석: {reflection}")

        # ✅ 예측 그래프 생성 및 이미지 저장
        fig, ax = plt.subplots()
        ax.scatter(x_raw, y_raw, color="blue", label="입력 데이터")
        ax.plot(run["x_plot"], run["y_pred"], color="red", label="예측선")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"예측 결과 {i+1}")
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
        if all(float(x).is_integer() for x in x_raw):
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        else:
            ax.xaxis.set_major_formatter(ScalarFormatter())

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, dpi=150, bbox_inches='tight')
            pdf.image(tmpfile.name, x=10, w=180)  # ✅ PDF에 이미지 삽입

        plt.close(fig)  # 리소스 정리

    pdf_output = bytes(pdf.output(dest='S'))

    st.download_button(
        label="📥 PDF 다운로드",
        data=pdf_output,
        file_name="ai_예측_학습지.pdf",
        mime="application/pdf"
    )


st.markdown("---")
st.success("✅ 예측 결과에 대한 해석을 모두 마쳤습니다!")
