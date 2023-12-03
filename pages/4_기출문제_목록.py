import streamlit as st
import sqlite3
import time



if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "search_subject" not in st.session_state:
    st.session_state.search_subject = None
    st.session_state.search_part = None
    st.session_state.search_request = None
    st.session_state.search_list = None
    st.session_state.fix_questnum = None

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

if "reg_subject" in st.session_state:
    st.session_state.reg_subject = None
    st.session_state.reg_part = None
    st.session_state.reg_question = None
    st.session_state.reg_qimage = None
    st.session_state.reg_atype = None
    st.session_state.reg_answers = None
    st.session_state.reg_rightindex = None

st.markdown("<h1 style='text-align: center;'기출문제 내역 페이지</h1>", unsafe_allow_html=True)
st.divider()

parts = {
    "회로이론": ("전기이론", "정현파 정류", "R-L-C 교류회로", "교류전력", "인덕턴스 및 백터궤적", "회로망", "대칭 n상 교류",
                        "대칭 좌표법", "비정현파 교류", "단자망", "라플라스 변환", "과도현상", "전달함수"),
    "제어공학": ("자동 제어계의 개요", "블록선도와 신호흐름선도", "자동 제어계의 시간영역 해석", "자동 제어계의 주파수영영 해석",
                "제어계의 안정도", "근궤적", "상태공간법", "시퀀스 제어"),
    "전기설비 기술기준": ( "공통사항", "전선로", "저압 전기설비", "고압.특고압 전기설비", "전기철도설비", "분산형전원설비", "전기설비기술기준"),
    "전기자기학": ("백터", "정전계", "도체계와 정전용량", "유전체와 특수현상", "전기회로", "정자계", "자성체와 자기회로", "전자유도와 인덕턴스", "전자계"),
    "전기기기": ("직류기", "동기기", "변압기", "유도기", "정류기"),
    "전력공학": ("전선로", "선로정수 및 코로나", "송전특성", "조상설비 및 전력 원선도", "고장계산", "중성점 접지방식과 유도장해", "이상전압 및 보호 계전방식", "변전소",
                "배전 방식 및 전기 공급 방식", "배전선로의 부하 특성 및 운용", "수력 발전", "화력 발전", "원자력 발전")

}
def fixQuest(questid):
    st.session_state.fix_questnum = questid

def convertTitle(origin):
    temp = origin.split(" ")
    result = ""
    for i in temp:
        result += "%s " % i
        if len(result) > 40: break
    return result 

def convertText(origin):
    temp = origin.replace("\n", " ")
    temp_arr = temp.split(" ")
    new_values = []
    startindex = 0
    breaknum = False
    while True:
        if breaknum: break
        value = ""
        for i in range(startindex, len(temp_arr)):
            if i >= len(temp_arr)-1:
                breaknum = True
            elif len(value) >= 30:
                startindex = i
                break
            value += (temp_arr[i] + "\\; ")
        new_values.append(value)
    result = ""
    for value in new_values:
        result += (value+" \\newline ")
    return result

st.markdown("""
    <style>
    [role=radiogroup]{
        gap: 1rem;
    }
    </style>
    """,unsafe_allow_html=True)


if st.session_state.is_logged:
    st.subheader("등록된 기출문제들의 목록들입니다.")
    if st.session_state.fix_questnum:
        st.write("업데이트가 필요한 기출문제(문제번호: %s)가 선택 되었습니다" % st.session_state.fix_questnum)
        st.write("등록및 수정 페이지에서 업데이트가 가능합니다.")
        st.write("다른 문제를 업데이트할 경후 조회 및 재선택 하시기를 바랍니다.")
    
    subject = st.selectbox("과목 선택", parts.keys(), index=None, placeholder="과목 중 한개를 선택 / 미선택시 전체 출력")
    query = None
    if subject:
        st.session_state.search_subject = subject
        if st.session_state.search_subject:
            query = "select id, subject, part, question, qimage, atype, answers, right_index from Quest where subject='%s'" % st.session_state.search_subject
            part = st.selectbox("과목 선택", parts[st.session_state.search_subject], index=None,  placeholder="%s 과목 중 한 챕터를 선택 해주세요/미선택시 전체 챕터 출력"%st.session_state.search_subject)
            if part:
                st.session_state.search_part = part
                if st.session_state.search_part:
                    query  += " and part='%s'" % st.session_state.search_part
                    
    col1, col2, col3 = st.columns([2, 2,7])
    with col1:
        btn_request = st.button("조회하기", use_container_width=True)
        if btn_request:
            if query != None:
                query = query + " order by id desc"
            else:
                query = "select id, subject, part, question, qimage, atype, answers, right_index from Quest order by id desc"
            db = sqlite3.connect("data.db")
            cu = db.cursor()
            cu.execute(query)
            data = cu.fetchall()
            db.close()
            st.session_state.search_list = data 
    with col2:
        btn_init = st.button("초기화", use_container_width=True)
        if btn_init:
            st.session_state.search_subject = None
            st.session_state.search_list = None


    st.divider()
    if st.session_state.search_list != None:
        data = st.session_state.search_list
        st.write("총 %s개의 기출문제가 검색됨" % len(data))

        for i in data:
            newtitle = convertTitle(i[3])
            expand = st.expander( r"$%s$" % newtitle, True ) 
            newvalue = convertText(i[3])
            expand.latex(r"%s"%newvalue)
            if len(i[4]) > 0 : 
                expand.write("문제 이미지")
                expand.image("./images/"+i[4])
            answers = i[6].split("|")
            if i[5] == "text":
                fix_answers = [ (r"$%s$"%answer).replace(" ", "\;")  for answer in answers ]
                expand.radio("", fix_answers, index=None, disabled=True, key="radio_"+str(i[0]))
            else:
                expand.write("보기 이미지")
                images = [ "./images/%s"%answer for answer in answers ]
                expand.image(images, width=150, caption=["보기1", "보기2", "보기3", "보기4"])
            if st.session_state.user_rank == "admin": 
                btn_fix = expand.button("수정하기", on_click=fixQuest, args=(i[0],), key="btn_"+str(i[0]))

        
else:
    st.subheader("해당 페이지는 로그인 후 접근 가능합니다.")
    st.subheader("왼쪽의 로그인 메뉴 클릭 후 헤당 페이지에서 로그인을 진행 부탁드립니다.")

hide_st_Style = """
<style>
    #MainMenu{visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_Style, unsafe_allow_html=True)