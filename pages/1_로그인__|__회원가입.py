import streamlit as st
import sqlite3
import datetime
import random
import smtplib
from email.mime.text import MIMEText

if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.user_nick = None
    st.session_state.user_rank = None
    st.session_state.user_lastlogin = None

if "user_select" not in st.session_state:
    st.session_state.user_select = "login"
    st.session_state.user_rerun = True

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

def sendMail(email, pwd):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("dukeout2@gmail.com", "krajvdrvalzacxvm")
    msg = """
        초기화된 비밀번호: %s
        위 비밀번호로 로그인 후 사용하실 비밀번호로 변경 부탁 드립니다.
    """ % pwd
    send_msg = MIMEText(msg)
    send_msg["Subject"] = "제목: 문제사이트 비밀번호 초기화 안내"
    smtp.sendmail("dukeout2@gmail.com", email, send_msg.as_string())
    smtp.quit()


st.markdown("<h1 style='text-align: center;'>로그인 | 회원가입 페이지</h1>", unsafe_allow_html=True)
st.divider()
col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

with col1:
    type_login = "primary" if st.session_state.user_select == "login" else "secondary"
    btn_login = st.button("로그인", use_container_width=True, type=type_login)
    if btn_login:
        st.session_state.user_select = "login"
        st.session_state.user_rerun = True

with col2:
    type_join = "primary" if st.session_state.user_select == "join" else "secondary"
    btn_join = st.button("회원가입", use_container_width=True, type=type_join)
    if btn_join:
        st.session_state.user_select = "join"
        st.session_state.user_rerun = True

with col3:
    type_initpwd = "primary" if st.session_state.user_select == "initpwd" else "secondary"
    btn_initpwd = st.button("비밀번호 초기화", use_container_width=True, type=type_initpwd)
    if btn_initpwd:
        st.session_state.user_select = "initpwd"
        st.session_state.user_rerun = True

with col4:
    type_changepwd = "primary" if st.session_state.user_select == "changepwd" else "secondary"
    btn_changepwd = st.button("비밀번호 변경", use_container_width=True, type=type_changepwd)
    if btn_changepwd:
        st.session_state.user_select = "changepwd"
        st.session_state.user_rerun = True

if st.session_state.user_rerun:
    st.session_state.user_rerun = False
    st.rerun()
user_select = st.session_state.user_select
match user_select:
    case "login":
        if st.session_state.is_logged:
            nick = st.session_state.user_nick
            rank = st.session_state.user_rank
            lastlogin = st.session_state.user_lastlogin
            st.subheader("%s 님(%s) 반갑습니다" % (nick, rank))
            st.write("마지막 로그인 시각: %s" % lastlogin)
            btn_logout = st.button("로그아웃")
            if btn_logout:
                st.session_state.is_logged = False
                st.session_state.user_email = None
                st.session_state.user_id = None
                st.session_state.user_nick = None
                st.session_state.user_rank = None
                st.rerun()
        else:
            with st.form("로그인"):
                _email = st.text_input("이메일", max_chars=40, placeholder="이메일을 입력바랍니다")
                _password = st.text_input("비밀번호", max_chars=40, placeholder="비밀번호를 입력바랍니다.", type="password")
                _submit = st.form_submit_button("로그인")

                if _submit:
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    cu.execute("select id, pwd, nick, rank from User where email='%s'" % _email)
                    data = cu.fetchall()
                    db.close()
                    if len(data) == 0 or data[0][1] != _password:
                        st.error("입력하신 이메일과 비밀번호를 다시 확인 바랍니다.")
                    else:
                        st.session_state.is_logged = True
                        st.session_state.user_email = _email
                        st.session_state.user_id = data[0][0]
                        st.session_state.user_nick = data[0][2]
                        st.session_state.user_rank = data[0][3]
                        st.session_state.user_lastlogin = datetime.datetime.now().__str__().split(".")[0]
                        st.rerun()
    case "join":
        if st.session_state.is_logged:
            st.subheader("해당 메뉴는 로그 아웃 후 이용 가능합니다.")
        else:
            with st.form("회원가입", clear_on_submit=True):
                _email = st.text_input("이메일", max_chars=40, placeholder='가입하실 이메일을 입력 바랍니다.')
                _nick = st.text_input("닉네임", max_chars=40, placeholder="사용하실 닉네임을 입력 바랍니다.")
                _pwd1 = st.text_input("비밀번호", max_chars=40, placeholder="사용하실 비밀번호를 입력 바랍니다", type="password")
                _pwd2 = st.text_input("비밀번호 확인", max_chars=40, placeholder="위에 입력한 비밀번호를 재입력 바랍니다", type="password")
                submit = st.form_submit_button("회원가입")
                if submit:
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    cu.execute("select email from User")
                    emails = [ i[0] for i in cu.fetchall() ]
                    if _email in emails:
                        st.error("이미 사용중인 이메일 주소입니다.")
                    elif _pwd1 != _pwd2:
                        st.error("비밀번호와 비밀번호 확인이 서로 다릅니다.")
                    else:
                        query = "insert into User(email, nick, pwd, rank) values('%s', '%s', '%s', 'User')" % (_email, _nick, _pwd1)
                        cu.execute(query)
                        db.commit()
                        st.success("회원가입이 완료되었습니다.\n로그인메뉴를 선택 후 로그인 부탁드립니다")
                    db.close()
    case "initpwd":
        if st.session_state.is_logged:
            st.subheader("해당 메뉴는 로그 아웃 후 이용 가능합니다.")
        else: 
            with st.form("비밀번호 초기화", clear_on_submit=True):
                _email = st.text_input("이메일", max_chars=40, placeholder="이메일을 입력바랍니다")
                _submit = st.form_submit_button("비밀번호 초기화")

                if _submit:
                    if st.session_state.is_logged:
                        st.subheader("해당 메뉴는 로그아웃 진행 후 이용 가능합니다.")
                    else:
                        db = sqlite3.connect("data.db")
                        cu = db.cursor()
                        cu.execute("select id, pwd, nick, rank from User where email='%s'" % _email)
                        data = cu.fetchall()
                        db.close()
                        if len(data) == 0:
                            st.error("입력하신 이메일 주소를 다시 확인 바랍니다.")
                        else:
                            initpwd = random.randint(100000, 999999)
                            db = sqlite3.connect("data.db")
                            cu = db.cursor()
                            cu.execute("update user set pwd='%s' where email='%s'"%(initpwd, _email))
                            db.commit()
                            db.close()
                            sendMail(_email, initpwd)
                            st.success("안내 메일 발송 완료. | 초기화된 비밀번호를 메일로 보내드렸습니다. 로그인 후 비밀번호를 변경 부탁드립니다.")      
    case "changepwd":
        if st.session_state.is_logged:
            with st.form("비밀번호 초기화", clear_on_submit=True):
                _pwd1 = st.text_input("신규 비밀번호", max_chars=40, placeholder="새로운 비밀번호를 입력바랍니다", type="password")
                _pwd2 = st.text_input("신규 비밀번호 확인", max_chars=40, placeholder="위의 비밀번호를 다시 한번 입력바랍니다", type="password")

                _submit = st.form_submit_button("비밀번호 변경하기")

                if _submit:
                    if _pwd1 != _pwd2:
                        st.error("서로 다른 비밀번호를 입력하였습니다.")
                    elif len(_pwd1) < 8:
                        st.error("비밀번호는 최소 8자리 이상 입력 바랍니다.")
                    else:
                        user_id = st.session_state.user_id
                        db = sqlite3.connect("data.db")
                        cu = db.cursor()
                        cu.execute("update user set pwd='%s' where id=%s" % (_pwd1, user_id))
                        db.commit()
                        db.close()
                        st.success("비밀번호가 업데이트 되었습니다 새로 로그인 바랍니다.")
                        st.session_state.is_logged = False
                        st.session_state.user_email = None
                        st.session_state.user_id = None
                        st.session_state.user_nick = None
                        st.session_state.user_rank = None
        else:
            st.subheader("해당 메뉴는 로그인 후 사용 가능합니다.")