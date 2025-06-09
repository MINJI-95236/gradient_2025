import streamlit as st
st.set_page_config(
    page_title="📕 데이터분석 (2) 분석 주제 선택",
    page_icon="📕",
    layout="centered"
)
st.title("📕 (2) 분석 주제 선택")

# 1단계에서 입력하지 않을 경우 경고 멘트 
if "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# 주제 입력
subject = st.text_area(
    "📌 어떤 데이터를 예측해보고 싶나요?",
    value=st.session_state.get("subject", ""),
    placeholder="예: 우리 반의 평균 키를 예측해보기",
    key="input_subject"  # 고유 key 설정
)

st.markdown("[🔎 국가통계포털 바로가기](https://kosis.kr/index/index.do)", unsafe_allow_html=True)

# 저장 버튼
if st.button("✅ 주제 저장"):
    if subject.strip():
        st.session_state.subject = subject
        st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 주제를 입력해주세요.")

if "subject" in st.session_state:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/8_📕_데이터분석_(3)_데이터입력.py")
