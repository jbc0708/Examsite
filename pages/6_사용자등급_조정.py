import streamlit as st
import sqlite3

if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "test_subject" in st.session_state:
    st.session_state.test_subject = None
    st.session_state.test_part = None
    st.session_state.test_range = None
    st.session_state.test_list = None
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

st.markdown("<h1 style='text-align: center;'>사용자 등급 변경 페이지</h1>", unsafe_allow_html=True)
st.divider()

def updateRank(id, rank):
    db = sqlite3.connect("data.db")
    cu = db.cursor()
    cu.execute("update user set rank='%s' where id=%s" % (rank, id))
    db.commit()
    db.close()
    st.toast("업데이트 성공")

if st.session_state.is_logged:
    if st.session_state.user_rank == "admin":
        st.subheader("사용자 등급 변경 페이지입니다.")
        db = sqlite3.connect("data.db")
        cu = db.cursor()
        cu.execute("select id, email, nick, rank from User order by rank asc, email asc")
        data = cu.fetchall()
        db.close()
        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
        rank_value = ['admin', 'user']
        for i in data:
            with col1:
                st.text_input("이메일", i[1])
            with col2:
                st.text_input("닉네임", i[2])
            with col3:
                rank = st.selectbox("등급", rank_value, rank_value.index(i[3]), key="fix_rankvalue%s" % i[0])
                if rank:
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    cu.execute("update user set rank='%s' where id=%s" % (rank, i[0]))
                    db.commit()
                    db.close()


    else:
        st.subheader("해당 페이지는 운영자만 접근 가능합니다.")
else:
    st.subheader("해당 페이지는 로그인 후 이용 가능합니다.")
    st.subheader("왼쪽에 로그인 메뉴를 클릭 후 해당 페이지에서 로그인을 진행 부탁드립니다.")