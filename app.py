import streamlit as st
import pandas as pd
import numpy as np

from time import sleep

import streamlit as st

st.set_page_config(
    page_title="(가제)경사하강법 ",
    page_icon="📊",
    layout="centered"
)

st.title("경사하강법이란?")
st.caption("인공지능의 원리! 경사하강법은~")

st.markdown("---")

st.subheader("📘 이 앱은 어떤 걸 하나요?")
st.markdown("""
- 직접 데이터를 입력하거나 파일로 올려서
- **산점도 그래프를 그리고**
- **1차 또는 2차 함수로 예측선**을 만들어볼 수 있어요!
- 예측 결과는 **PDF로 저장도 가능**해요.
""")

st.subheader("🧭 어떻게 진행되나요?")
st.markdown("""
1. 왼쪽 메뉴에서 **[1단계: 기본 정보 입력]** 으로 이동해 정보를 입력하세요.  
2. 이후 단계를 차례대로 따라가면 됩니다!
""")

st.success("왼쪽의 📘 메뉴에서 1단계부터 시작해보세요!")