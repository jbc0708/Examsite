import streamlit as st


if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "test_subject" in st.session_state:
    st.session_state.test_subject = None
    st.session_state.test_part = None
    st.session_state.test_list = None
    st.session_state.test_range = None
    st.session_state.test_stime = None
    st.session_state.test_etime = None
    st.session_state.test_submit = None
    st.session_state.test_current = None

if "history_subject" in st.session_state:
    st.session_state.history_subject = None
    st.session_state.history_part = None
    st.session_state.history_list = None
    st.session_state.history_range = None

if "search_subject" in st.session_state:
    st.session_state.search_subject = None
    st.session_state.search_part = None
    st.session_state.search_request = None
    st.session_state.search_list = None
    st.session_state.fix_questnum = None

if "reg_subject" in st.session_state:
    st.session_state.reg_subject = None
    st.session_state.reg_part = None
    st.session_state.reg_question = None
    st.session_state.reg_qimage = None
    st.session_state.reg_atype = None
    st.session_state.reg_answers = None
    st.session_state.reg_rightindex = None
    st.session_state.fix_questnum = None


st.markdown("<h1 style='text-align: center;'>소개 페이지</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>사이드 메뉴가 보이지 않으면 왼쪽 상단에 화살표 클릭!!</h6>", unsafe_allow_html=True)
st.divider()

st.subheader("사이트 제작 동기")
st.write("해당 사이트는 전기기능사/전기기사(산업기사) 취득 목적으로 만들었습니다.")
st.write("얼마나 공부를 한 상태인지 확인하는게 주된 목적입니다.")
st.subheader("사이트 이용 방법")
st.write("사이드 메뉴중 모의시험응시,시험응시내역,기출문제내역은 회원가입 후 이용가능합니다.")
st.write("기출문제등록(수정) 및 사용자등급조정은 운영자 등급만 가능합니다.")
st.subheader("사이트 제작 일자")
st.write("2023-10-27 ~ 2023-10-28")