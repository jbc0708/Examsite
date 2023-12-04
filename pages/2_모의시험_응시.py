import streamlit as st
import sqlite3
import datetime
import random

if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "test_subject" not in st.session_state:
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

if "search_subject" in st.session_state:
    st.session_state.reg_subject = None
    st.session_state.reg_part = None
    st.session_state.reg_question = None
    st.session_state.reg_qimage = None
    st.session_state.reg_atype = None
    st.session_state.reg_answers = None
    st.session_state.reg_rightindex = None
    st.session_state.fix_questnum = None

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
            value += (temp_arr[i] + " \;")
        new_values.append(value)
    result = ""
    for value in new_values:
        result += (value+"\\newline ")
    return result

def makeTest(exam, exam_info):

    choice_info = {}
    for i in exam_info:
        gids = i[0].split(",")
        rids = i[1].split(",")
        for gid in gids:
            if gid in choice_info:
                choice_info[gid]["cnt_gid"] += 1
            else:
                choice_info[gid] = {"cnt_gid": 1, "cnt_rid": 0}
        print(rids)
        if rids != [""]:
            for rid in rids:
                choice_info[rid]["cnt_rid"] += 1

    test_exam = []
    #id, subject, part, qtype, question, qimage, atype, answers, right_index, choice, per

    for i in exam:
        answers = i[7].split("|")
        right_index_before = i[8]
        right_target = answers[right_index_before]
        random.shuffle(answers)
      
        quest =  list(i[:7])
        quest.append(answers)
        if i[6] == 'text':
            quest.append(right_target)
        else:
            arr = ['보기1', '보기2', '보기3', '보기4']
            quest.append(arr[answers.index(right_target)])

        quest.append("")
        q_id = str(i[0])
        if (q_id in list(choice_info.keys())):
            target = choice_info[q_id]
            per = int(target["cnt_rid"]/target["cnt_gid"]*100)
            quest.append("%s %%"%per)
        else:
            quest.append("")
        test_exam.append(quest)
    return test_exam


st.markdown("<h1 style='text-align: center;'모의시험 페이지</h1>", unsafe_allow_html=True)
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
    st.subheader("모의시험 응시 페이지입니다.")
    if st.session_state.test_submit:
        st.subheader("응시하신 모의시험이 제출되었습니다.")
        st.subheader("결과는 메뉴-시험응시 내역 페이지에서 조회가 가능합니다.")
    elif st.session_state.test_list:
        data = st.session_state.test_list
        test_range = "과목: %s" % st.session_state.test_subject if st.session_state.test_subject else "과목: 전체"
        test_range += " 파트: %s" % st.session_state.test_part if st.session_state.test_part else " 파트: 전체"

        st.session_state.test_range = test_range
        st.write("문제 출제 범위 - %s" % test_range)
        st.write("총 %s개의 기출문제가 출제됨" % len(data))
        #id, subject, part, qtype, question, qimage, atype, answers, right_answer
        current = st.session_state.test_current
        target = data[current]
        title = "문제: %3s / %3s " % (current + 1, len(data))
        if target[-1] != "": title += " 정답률: %s" % target[-1]
        expand = st.expander(title, True)
        newvalue = convertText(target[4])
        expand.latex(r"%s"%newvalue)
        if len(target[5]) > 0:
            expand.image("./images/"+target[5])
        answers = target[7]
        if target[6] == "text":
            fix_answers = [ r"$%s$"%answer.replace(" ","\;")  for answer in answers ]
            index_choice = None if target[-2] == "" else fix_answers.index(target[-2])
            choice = expand.radio(" ", fix_answers, index=index_choice, key="radio_%s" % current)
        else:
            expand.write("보기 이미지")
            images = [ "./images/%s"%answer for answer in answers ]
            captions = ["보기1", "보기2", "보기3", "보기4"]
            expand.image(images, width=150, caption=captions)
            index_choice = None if target[-2] == "" else captions.index(target[-2])
            choice = expand.radio(" ", captions, index=index_choice, key="radio_%s" % st.session_state.test_current)
        if choice: st.session_state.test_list[current][-2] = choice
        
        col1, col2, col3 = st.columns([2,2,11])

        with col1:
            if st.session_state.test_current > 0:
                btn_pre_label = "이전문제"
            else:
                btn_pre_label = "다음문제"
            btn_pre = st.button(btn_pre_label)
            if btn_pre: 
                if btn_pre_label == "이전문제":
                    st.session_state.test_current -= 1
                else:
                    st.session_state.test_current += 1
                st.rerun()

        with col2:
            if st.session_state.test_current == len(data) - 1:
                btn_submit = st.button("제출하기")
                if btn_submit:
                    if st.session_state.test_submit == None:
                        st.session_state.test_submit = True
                        st.session_state.test_etime = datetime.datetime.now().__str__().split(".")[0]
                        data = st.session_state.test_list 
                        gids = []
                        rids = []
                        for i in range(len(data)):
                            info = data[i]
                            gids.append(info[0])
                            fixanswer = info[-2].replace("\;", " ").replace("$", "")
                            print(i+1, info[-3], fixanswer)
                            if fixanswer == info[-3]: rids.append(info[0])
                        db = sqlite3.connect("data.db")
                        cu = db.cursor()
                        uid = st.session_state.user_id
                        dayinfo = st.session_state.test_etime.split(" ")
                        day = dayinfo[0]
                        stime = st.session_state.test_stime.split(" ")[1]
                        etime = dayinfo[1]
                        test_range = st.session_state.test_range
                        gids_str = str(gids).replace("[", "").replace("]","").replace(" ","")
                        rids_str = str(rids).replace("[", "").replace("]","").replace(" ","")
                        query = "insert into history(uid, day, stime, etime, test_range, gids,rids) values(%s,'%s','%s','%s','%s', '%s', '%s')" % (
                            uid, day, stime, etime, test_range, gids_str, rids_str
                        )
                        cu.execute(query)
                        db.commit()
                        db.close()
                        st.session_state.test_submit = True
                        st.rerun()
            elif st.session_state.test_current > 0:
                btn_next = st.button("다음문제")
                if btn_next:
                    st.session_state.test_current += 1
                    st.rerun()
    else:
        subject = st.selectbox("과목 선택", parts.keys(), index=None, placeholder="과목 선택 / 미선택시 전체과목 응시", key="sel_subject")
        if subject:
            st.session_state.test_subject = subject
            if st.session_state.test_subject:
                st.session_state.test_part = None
                part = st.selectbox("챕터 선택", parts[st.session_state.test_subject], index=None,  placeholder="챕터 중 한개를 선택 해주세요/미선택시 전체챕터 응시")
                if part:
                    st.session_state.test_part = part
                

        col1, col2, col3 = st.columns([2, 2, 7])

        with col1:
            btn_request = st.button("응시하기", use_container_width=True)

            if btn_request:
                db = sqlite3.connect("data.db")
                cu = db.cursor()

                query = "select id, subject, part, qtype, question, qimage, atype, answers, right_index from quest"
                addquery = ""
                st.session_state.test_stime = datetime.datetime.now().__str__().split(".")[0]
                exam = []

                if st.session_state.test_subject:
                    addquery = " where subject='%s'" % st.session_state.test_subject
                    cnt = 100
                    if st.session_state.test_part:
                        addquery = addquery + " and part='%s'" % st.session_state.test_part
                        cnt = 40
                    addquery = addquery + " order by random() limit %s" % cnt
                    cu.execute(query+addquery)
                    exam = cu.fetchall()           
                else:
                    for insubject in parts:
                        addquery = " where subject='%s' order by random() limit 20"% insubject
                        cu.execute(query + addquery)
                        data = cu.fetchall()
                        for i in data:
                            exam.append(i)
                cu.execute("select gids, rids from history where uid=%s"%st.session_state.user_id)
                exam_info = cu.fetchall()
                exam_list = makeTest(exam, exam_info)
                st.session_state.test_list = exam_list
                st.session_state.test_current = 0
                st.rerun()
        with col2:
            btn_init = st.button("초기화", use_container_width=True)
            if btn_init:
                st.session_state.test_subject = None
                st.session_state.test_part = None
                st.session_state.test_list = None
                st.session_state.test_range = None
                st.session_state.test_stime = None
                st.session_state.test_etime = None
                st.session_state.test_point = None
                st.session_state.test_submit = None
                st.session_state.test_current = None


        st.divider()
        
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