import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import os

# ✅ 한글 폰트 설정
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

st.title("📊 3단계: 데이터 입력 (표 형태)")

# 🔒 이전 단계 확인
if "name" not in st.session_state or "subject" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

with st.expander("📘 사용 순서 안내 (클릭해서 열기)"):
    st.markdown("""
    1. **x축/y축 이름을 먼저 입력하세요.**  
       예: `공부시간`, `성적` 등

    2. **표에 데이터를 입력하세요.**  
       숫자만 입력 가능해요. 한 줄에 하나의 데이터쌍을 입력합니다.

    3. **[💾 데이터 저장] 버튼을 꼭 누르세요.**  
       저장하지 않으면 입력한 데이터가 사라질 수 있어요.

    4. **[📊 산점도 보기] 버튼으로 시각화 결과를 확인하세요.**

    5. 모든 조건을 만족하면 [➡️ 다음] 버튼이 활성화됩니다.
    """)

st.warning("""
⚠️ **주의사항**  
x축과 y축 이름, 데이터를 입력한 후에는 반드시 **[💾 데이터 저장] 버튼**을 눌러주세요.  
저장을 완료하지 않으면 **x/y축 이름 변경이 제대로 적용되지 않을 수 있습니다.**
""")

# ✅ x, y 라벨 입력
default_x = "예: 공부 시간"
default_y = "예: 성적"

x_label = st.text_input("x축 이름", value=st.session_state.get("x_label", ""), placeholder=default_x)
y_label = st.text_input("y축 이름", value=st.session_state.get("y_label", ""), placeholder=default_y)

# ✅ 라벨이 둘 다 없으면 아래 UI 숨기고 안내 문구만 출력
if not x_label.strip() or not y_label.strip():
    st.markdown("✅ x/y축 이름을 입력하면 아래에 표가 나타납니다.")
    st.stop()

# ✅ 라벨 저장
st.session_state.x_label = x_label
st.session_state.y_label = y_label

# ✅ 초기 테이블
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})

safe_x_label = x_label
safe_y_label = y_label
display_data = st.session_state.table_data.rename(columns={"x": safe_x_label, "y": safe_y_label})

# ✅ 표 UI
edited_data = st.data_editor(
    display_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        x_label: st.column_config.NumberColumn(label=x_label, width="small"),
        y_label: st.column_config.NumberColumn(label=y_label, width="small")
    },
    key="data_editor"
)

# 상태 키 초기화
if "show_plot" not in st.session_state:
    st.session_state.show_plot = False

# 📌 버튼 영역
col1, col2, col3 = st.columns([1, 1, 1])

# 💾 데이터 저장
with col1:
    if st.button("💾 데이터 저장"):
        try:
            st.session_state.x_label = x_label
            st.session_state.y_label = y_label
            updated_df = edited_data.rename(columns={x_label: "x", y_label: "y"})
            st.session_state.table_data = updated_df
            st.success("✅ 데이터가 저장되었습니다!")
        except Exception as e:
            st.warning("저장 중 오류: " + str(e))

# 📊 산점도 보기
with col2:
    if st.button("📊 산점도 보기"):
        st.session_state.show_plot = True

# 🔄 초기화
with col3:
    if st.button("🔄 데이터 초기화"):
        st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})
        st.session_state.show_plot = False
        st.success("모든 데이터가 초기화되었습니다.")

# 📈 산점도
if st.session_state.show_plot:
    try:
        df = st.session_state.table_data.dropna()
        xs = df["x"].tolist()
        ys = df["y"].tolist()
        valid_data = [(x, y) for x, y in zip(xs, ys) if x != 0 or y != 0]

        if len(valid_data) < 2:
            st.warning("⚠️ 데이터는 2쌍 이상 필요해요.")
        else:
            x_valid, y_valid = zip(*valid_data)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x_valid, y_valid)

            if font_prop:
                ax.set_xlabel(x_label, fontproperties=font_prop)
                ax.set_ylabel(y_label, fontproperties=font_prop)
                ax.set_title("산점도 확인하기", fontproperties=font_prop)
            else:
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_title("산점도 확인하기")

            ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))

            import matplotlib.ticker as mtick
            ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
            if all(float(x).is_integer() for x in x_valid):
                ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
            else:
                ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

            fig.tight_layout()
            st.pyplot(fig)

            st.session_state.x_values = list(x_valid)
            st.session_state.y_values = list(y_valid)

            st.markdown("### ✏️ 산점도를 보고 분석 내용을 작성해보세요:")
            analysis_input = st.text_area(
                label="📌 분석 내용",
                value=st.session_state.get("analysis_text", ""),
                placeholder="예: 공부 시간이 많을수록 성적이 높아지는 경향이 보입니다.",
                height=150
            )
            st.session_state.analysis_text = analysis_input

            st.success("✅ 다음 단계로 이동 가능해요.")
    except Exception as e:
        st.error("산점도 오류: " + str(e))

# ⏩ 다음 단계
if "x_values" in st.session_state and "y_values" in st.session_state:
    colA, colB, colC = st.columns([3, 1, 1])
    with colC:
        if st.button("➡️ 다음"):
            st.switch_page("pages/4_4️⃣_예측결과.py")
