import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

# ✅ 한글 폰트 설정 (서버 포함)
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

st.title("📊 3단계: 데이터 입력 (표 형태)")

# 🔒 이전 단계 확인
if "name" not in st.session_state or "subject" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# ✅ x, y 라벨: 최초 1회만 초기화, 이후 session_state로 유지
if "x_label" not in st.session_state:
    st.session_state.x_label = "공부 시간"
if "y_label" not in st.session_state:
    st.session_state.y_label = "성적"

# 📌 라벨 입력
st.session_state.x_label = st.text_input("x축 이름", value=st.session_state.x_label, key="input_x_label")
st.session_state.y_label = st.text_input("y축 이름", value=st.session_state.y_label, key="input_y_label")

x_label = st.session_state.x_label
y_label = st.session_state.y_label

st.info("✏️ **x축 또는 y축 이름을 바꾸더라도 데이터는 유지됩니다. 단, [📊 산점도 보기] 버튼을 다시 눌러야 반영돼요!**")

# ✅ 표 데이터 초기화 (항상 내부적으로는 'x', 'y' 사용)
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})

# 표 표시용 라벨 적용 데이터 생성
display_data = st.session_state.table_data.rename(columns={"x": x_label, "y": y_label})

st.markdown("📋 아래 표에 데이터를 입력하세요 (숫자 2개 이상 필요)")

# 🔢 표 입력창
edited_data = st.data_editor(
    display_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        x_label: st.column_config.NumberColumn(label=x_label, width="small"),
        y_label: st.column_config.NumberColumn(label=y_label, width="small")
    }
)
try:
    st.session_state.table_data = edited_data.rename(columns={x_label: "x", y_label: "y"})
except:
    pass  # 오류 무시 (초기 로딩시 열이 안 맞을 수도 있음)
# 📊 산점도 보기
if st.button("📊 산점도 보기"):
    try:
        df = edited_data.rename(columns={x_label: "x", y_label: "y"}).dropna()
        xs = df["x"].tolist()
        ys = df["y"].tolist()
        valid_data = [(x, y) for x, y in zip(xs, ys) if x != 0 or y != 0]

        if len(valid_data) < 2:
            st.warning("⚠️ 데이터는 2쌍 이상 필요해요.")
        else:
            x_valid, y_valid = zip(*valid_data)
            fig, ax = plt.subplots()
            ax.scatter(x_valid, y_valid)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title("산점도 확인하기")
            ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
            if all(float(x).is_integer() for x in x_valid):
                ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
            else:
                ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
            st.pyplot(fig)

            # ✅ session_state 저장
            st.session_state.x_values = list(x_valid)
            st.session_state.y_values = list(y_valid)
            st.session_state.table_data = df  # 'x', 'y'로 저장

            st.success("✅ 데이터가 저장되었습니다! 다음 단계로 이동하세요.")
    except Exception as e:
        st.error(f"데이터 처리 중 오류: {e}")

if "x_values" in st.session_state and "y_values" in st.session_state:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/4_4️⃣_예측결과.py")

