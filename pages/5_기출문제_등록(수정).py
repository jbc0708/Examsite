import streamlit as st
import sqlite3



if "is_logged" not in st.session_state:
    st.session_state.is_logged = False
    
if "reg_subject" not in st.session_state:
    st.session_state.reg_subject = None
    st.session_state.reg_part = None
    st.session_state.reg_question = None
    st.session_state.reg_qimage = None
    st.session_state.reg_atype = None
    st.session_state.reg_answers = None
    st.session_state.reg_rightindex = None
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

if "search_subject" in st.session_state:
    st.session_state.search_subject = None
    st.session_state.search_part = None
    st.session_state.search_request = None
    st.session_state.search_list = None

st.markdown("<h1 style='text-align: center;'> 기출문제 등록 및 수정 페이지</h1>", unsafe_allow_html=True)
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


if st.session_state.is_logged:
    if st.session_state.user_rank == "admin":
        st.subheader("기출문제 등록/수정 페이지입니다.")
        if st.session_state.fix_questnum != None:
            db = sqlite3.connect("data.db")
            cu = db.cursor()
            cu.execute("select subject, part, qtype, question, qimage, atype, answers, right_index from Quest where id = %s" % st.session_state.fix_questnum)
            data = cu.fetchall()[0]
            db.close()
            
            subject_values = list(parts.keys())
            subject = st.selectbox("과목", subject_values, subject_values.index(data[0]))
            if subject:
                st.session_state.reg_subject = subject
                part_values = list(parts[subject])
                part = st.selectbox("과목", part_values, part_values.index(data[1]))
                if part:
                    st.session_state.reg_part = part
            qtype = st.selectbox("문제유형타입", ("암기", "계산") )
            question = st.text_area("문제", data[3])
            st.session_state.reg_question = question if question else None

            qimage_label = "문제용보기(등록)" if data[4] == "" else "문제용보기(수정)"
            qimage = st.file_uploader(qimage_label, type=["png", "jpg", "jpeg"])
            st.session_state.reg_qimage = qimage if qimage else None

            atype_dict = {"text": "텍스트", "image": "이미지"}
            atype_values = ["텍스트", "이미지"]
            _atype = st.selectbox("보기유형타입", atype_values, atype_values.index(atype_dict[data[5]]))
            atypes = {"텍스트": "text", "이미지": "image"}
            atype = atypes[_atype]
            st.session_state.reg_atype = atype
            if _atype == "텍스트":
                answers = data[6].split("|")
                answer1 = st.text_input("보기1", answers[0])
                answer2 = st.text_input("보기2", answers[1])
                answer3 = st.text_input("보기3", answers[2])
                answer4 = st.text_input("보기4", answers[3])
            else:
                answer1 = st.file_uploader("보기1")
                answer2 = st.file_uploader("보기2")
                answer3 = st.file_uploader("보기3")
                answer4 = st.file_uploader("보기4")
            right_index_values = ["보기1", "보기2", "보기3", "보기4"]
            right_index = st.selectbox("정답번호", right_index_values, data[7], placeholder="정답을 선택 해주세요")
            st.session_state.reg_rightindex = right_index if right_index else None

            btn_submit = st.button("등록하기")
            if btn_submit:
                doSave = True
                if len(question.replace(" ","")) == 0:
                    doSave = False
                    st.error("문제를 입력하세요")
                elif right_index == None:
                    doSave = False
                    st.error("정답번호를 선택하세요")

                if atype == "text":
                    if len(answer1.replace(" ", "")) == "" or answer1 == None:
                        doSave = False
                        st.error("보기1을 입력하세요")
                    elif len(answer2.replace(" ", "")) == "" or answer2 == None:
                        doSave = False
                        st.error("보기2를 입력하세요")
                    elif len(answer3.replace(" ", "")) == "" or answer3 == None:
                        doSave = False
                        st.error("보기3을 입력하세요")
                    elif len(answer4.replace(" ", "")) == "" or answer4 == None:
                        doSave = False
                        st.error("보기4를 입력하세요")
                else:
                    if answer1 == None:
                        doSave = False
                        st.error("보기1을 입력하세요")
                    elif answer2 == None:
                        doSave = False
                        st.error("보기2를 입력하세요")
                    elif answer3 == None:
                        doSave = False
                        st.error("보기3을 입력하세요")
                    elif answer4 == None:
                        doSave = False
                        st.error("보기4를 입력하세요")

                if doSave:
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    query = "update quest set subject='%s', part='%s', qtype='%s', question='%s'" % (subject, part, qtype, r"""%s"""%question)
                    if qimage:
                        filename = "%s_q.%s" % (st.session_state.fix_questnum, qimage.name.split(".")[-1])
                        query = query + ", qimage='%s_q.%s'" % (st.session_state.fix_questnum, qimage.name.split(".")[-1]) 
                        byte_data = qimage.read()
                        f = open("./images/%s" % filename, "wb")
                        f.write(byte_data)
                        f.close()
                    if atype == "text":
                        answers = r"%s|%s|%s|%s" % (answer1, answer2, answer3, answer4)
                    else:
                        answers = ""
                        filename1 = "%s_a_1.%s" % (st.session_state.fix_questnum, answer1.name.split(".")[-1])
                        answers += "%s|" % filename1
                        byte_data1 = answer1.read()
                        f = open("./images/%s" % filename1, "wb")
                        f.write(byte_data1)
                        f.close()

                        filename2 = "%s_a_2.%s" % (st.session_state.fix_questnum, answer2.name.split(".")[-1])
                        answers += "%s|" % filename2
                        byte_data2 = answer2.read()
                        f = open("./images/%s" % filename2, "wb")
                        f.write(byte_data2)
                        f.close()

                        filename3 = "%s_a_3.%s" % (st.session_state.fix_questnum, answer3.name.split(".")[-1])
                        answers += "%s|" % filename3
                        byte_data3 = answer3.read()
                        f = open("./images/%s" % filename3, "wb")
                        f.write(byte_data3)
                        f.close()

                        filename4 = "%s_a_4.%s" % (st.session_state.fix_questnum, answer4.name.split(".")[-1])
                        answers += "%s" % filename4
                        byte_data4 = answer4.read()
                        f = open("./images/%s" % filename4, "wb")
                        f.write(byte_data4)
                        f.close()
                    query += """, atype="%s", answers="%s" """ % (atype, answers)
                    
                    query += ", right_index=%s where id=%s" % (right_index_values.index(right_index), st.session_state.fix_questnum)
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    cu.execute(query)
                    db.commit()
                    db.close()
                    st.session_state.fix_questnum = None
                    st.success("기출문제 업데이트가 완료되었습니다.")

        else:
            subject = st.selectbox("과목", parts.keys())
            if subject:
                st.session_state.reg_subject = subject
                part = st.selectbox("챕터", parts[subject])
                if part:
                    st.session_state.reg_part = part
            qtype = st.selectbox("뮨제유형타입", ("암기", "계산"))
            question = st.text_area("문제", "", height=150)
            st.session_state.reg_question = question if question else None

            qimage = st.file_uploader("문제용보기(등록)", type=["png", "jpg", "jpeg"])
            st.session_state.reg_qimage = qimage if qimage else None

            _atype = st.selectbox("보기유형타입", ["텍스트", "이미지"])
            atypes = {"텍스트": "text", "이미지": "image"}
            atype = atypes[_atype]
            st.session_state.reg_atype = atype
            if _atype == "텍스트":
                answer1 = st.text_input("보기1")
                answer2 = st.text_input("보기2")
                answer3 = st.text_input("보기3")
                answer4 = st.text_input("보기4")
            else: 
                answer1 = st.file_uploader("보기1")
                answer2 = st.file_uploader("보기2")
                answer3 = st.file_uploader("보기3")
                answer4 = st.file_uploader("보기4")

            right_index = st.selectbox("정답번호", ["보기1", "보기2", "보기3", "보기4"], None, placeholder="정답을 선택 해주세요")
            st.session_state.reg_rightindex = right_index if right_index else None


        
            btn_submit = st.button("등록하기")
            if btn_submit:
                doSave = True
                if len(question.replace(" ","")) == 0:
                    doSave = False
                    st.error("문제를 입력하세요")
                elif right_index == None:
                    doSave = False
                    st.error("정답번호를 선택하세요")
                if atype == "text":
                    if len(answer1.replace(" ", "")) == "" or answer1 == None:
                        doSave = False
                        st.error("보기1을 입력하세요")
                    elif len(answer2.replace(" ", "")) == "" or answer2 == None:
                        doSave = False
                        st.error("보기2를 입력하세요")
                    elif len(answer3.replace(" ", "")) == "" or answer3 == None:
                        doSave = False
                        st.error("보기3을 입력하세요")
                    elif len(answer4.replace(" ", "")) == "" or answer4 == None:
                        doSave = False
                        st.error("보기4를 입력하세요")
                else:
                    if answer1 == None:
                        doSave = False
                        st.error("보기1을 입력하세요")
                    elif answer2 == None:
                        doSave = False
                        st.error("보기2를 입력하세요")
                    elif answer3 == None:
                        doSave = False
                        st.error("보기3을 입력하세요")
                    elif answer4 == None:
                        doSave = False
                        st.error("보기4를 입력하세요")
                
                if doSave:
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    cu.execute("select max(id) from Quest")
                    data = cu.fetchall()
                    id = data[0][0] + 1 if data[0][0] != None else 1
                    insert = "insert into Quest(subject,part,qtype,question"
                    values = "values('%s','%s','%s','%s'" % (subject,part,qtype,r"""%s"""%question)
                    if qimage:
                        filename = "%s_q.%s" % (id, qimage.name.split(".")[-1])
                        insert += ", qimage"
                        values += ", '%s'" % filename
                        byte_data = qimage.read()
                        f = open("./images/%s" % filename, "wb")
                        f.write(byte_data)
                        f.close()
                    if atype == "text":
                        answers = r"%s|%s|%s|%s" % (answer1, answer2, answer3, answer4)
                    else:
                        answers = ""
                        filename1 = "%s_a_1.%s" % (id, answer1.name.split(".")[-1])
                        answers += "%s|" % filename1
                        byte_data1 = answer1.read()
                        f = open("./images/%s" % filename1, "wb")
                        f.write(byte_data1)
                        f.close()

                        filename2 = "%s_a_2.%s" % (id, answer2.name.split(".")[-1])
                        answers += "%s|" % filename2
                        byte_data2 = answer2.read()
                        f = open("./images/%s" % filename2, "wb")
                        f.write(byte_data2)
                        f.close()

                        filename3 = "%s_a_3.%s" % (id, answer3.name.split(".")[-1])
                        answers += "%s|" % filename3
                        byte_data3 = answer3.read()
                        f = open("./images/%s" % filename3, "wb")
                        f.write(byte_data3)
                        f.close()

                        filename4 = "%s_a_4.%s" % (id, answer4.name.split(".")[-1])
                        answers += "%s" % filename4
                        byte_data4 = answer4.read()
                        f = open("./images/%s" % filename4, "wb")
                        f.write(byte_data4)
                        f.close()
                    insert += ", atype, answers, right_index) "
                    right_index_values = ["보기1", "보기2", "보기3", "보기4"]
                    values += ", '%s', '%s', %s)" % (atype, answers, right_index_values.index(right_index))
                    db = sqlite3.connect("data.db")
                    cu = db.cursor()
                    
                    cu.execute(insert+values)
                    db.commit()
                    db.close()
                    st.session_state.fix_questnum = None
                    st.success("기출문제 등록이 완료되었습니다.")    
                
    else:
        st.subheader("해당 페이지는 운영자만 접근 가능합니다.")
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