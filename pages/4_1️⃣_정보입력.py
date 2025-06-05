import streamlit as st

st.title("📘 1단계: 기본 정보 입력")

name = st.text_input("이름", value=st.session_state.get("name", ""), key="input_name")
student_id = st.text_input("학번", value=st.session_state.get("student_id", ""), key="input_id")
school = st.text_input("학교", value=st.session_state.get("school", ""), key="input_school")
date = st.date_input("날짜 선택", value=st.session_state.get("date"), key="input_date")

# 저장 버튼
if st.button("✅ 저장하기"):
    if name and student_id and school:
        # session_state에 저장
        st.session_state.name = name
        st.session_state.student_id = student_id
        st.session_state.school = school
        st.session_state.date = str(date)

        st.success("✅ 정보가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")

if "name" in st.session_state:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/4_2️⃣_분석주제.py")
