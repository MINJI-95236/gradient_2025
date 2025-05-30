import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator


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

st.title("📊 3단계: 데이터 입력 (표 형태)")

# 🔒 이전 단계 확인
if "name" not in st.session_state or "subject" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# ✅ x, y 라벨 초기화
# 기본 라벨 (예: placeholder 용)
default_x = "예: 공부 시간"
default_y = "예: 성적"

# 세션에서 꺼내되, 없으면 빈 문자열로
x_label = st.text_input("x축 이름", value=st.session_state.get("x_label", ""), placeholder=default_x)
y_label = st.text_input("y축 이름", value=st.session_state.get("y_label", ""), placeholder=default_y)

# 빈 값일 경우 기본 라벨 사용 (표 컬럼 에러 방지용)
safe_x_label = x_label if x_label.strip() else default_x
safe_y_label = y_label if y_label.strip() else default_y

# session_state에는 입력된 값만 저장
if x_label.strip():
    st.session_state.x_label = x_label
if y_label.strip():
    st.session_state.y_label = y_label


#st.info("✏️ 데이터는 저장하지 않으면 유지되지 않아요!")

# ✅ table_data 최초 초기화
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})

# 🔁 표시용 데이터프레임 (항상 내부적으로는 x/y)
display_data = st.session_state.table_data.rename(columns={"x": safe_x_label, "y": safe_y_label})
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

# 🧾 표 UI만 출력 (값 반영은 저장 버튼 눌렀을 때만)
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

# 💾 데이터 저장
# 상태 저장용 키 초기화
if "show_plot" not in st.session_state:
    st.session_state.show_plot = False

# 📌 버튼 3개 정렬
col1, col2, col3 = st.columns([1, 1, 1])

# 💾 데이터 저장
with col1:
    if st.button("💾 데이터 저장"):
        try:
            updated_df = edited_data.rename(columns={x_label: "x", y_label: "y"})
            st.session_state.table_data = updated_df
            st.success("✅ 데이터가 저장되었습니다!")
        except Exception as e:
            st.warning("저장 중 오류: " + str(e))

# 📊 산점도 보기 버튼 (클릭 시 상태 플래그 켜기)
with col2:
    if st.button("📊 산점도 보기"):
        st.session_state.show_plot = True

# 🔄 데이터 초기화
with col3:
    if st.button("🔄 데이터 초기화"):
        st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})
        st.session_state.show_plot = False
        st.success("모든 데이터가 초기화되었습니다.")

# 📈 산점도 그리기 (버튼 아래에 크게 출력)
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

            st.success("✅ 다음 단계로 이동 가능해요.")
    except Exception as e:
        st.error("산점도 오류: " + str(e))


# ⏩ 다음 단계로 이동
if "x_values" in st.session_state and "y_values" in st.session_state:
    colA, colB, colC = st.columns([3, 1, 1])
    with colC:
        if st.button("➡️ 다음"):
            st.switch_page("pages/4_4️⃣_예측결과.py")
