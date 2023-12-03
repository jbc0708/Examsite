import streamlit as st
import sqlite3
import pandas as pd

if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

if "history_subject" not in st.session_state:
    st.session_state.history_subject = None
    st.session_state.history_part = None
    st.session_state.history_list = None
    st.session_state.history_range = None

if "test_subject" in st.session_state:
    st.session_state.test_subject = None
    st.session_state.test_part = None
    st.session_state.test_range = None
    st.session_state.test_list = None
    st.session_state.test_stime = None
    st.session_state.test_etime = None
    st.session_state.test_submit = None
    st.session_state.test_current = None

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

st.markdown("<h1 style='text-align: center;'시험 응시 내역 페이지</h1>", unsafe_allow_html=True)
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
    st.session_state.history_subject = None
    st.session_state.history_part = None
    st.subheader("그동안 진행했던 모의테스트 결과의 기록들 입니다.")
    subject = st.selectbox("과목 선택", parts.keys(), index=None, placeholder="과묵 중 한개를 선택하세요/미선택시 응시내역 전체 출력")
    if subject:
        st.session_state.history_subject = subject
        if st.session_state.history_subject:
            part = st.selectbox("챕터 선택", parts[st.session_state.history_subject], index=None,  placeholder="챕터 중 한개를 선택 해주세요/미선택시 해당과목 전체챕터 대상 응시내역 출력")
            if part:
                st.session_state.history_part = part

    col1, col2= st.columns([2,  9])
    with col1:
        btn_request = st.button("조회하기", use_container_width=True)

        if btn_request:
            query = "select  day, stime, etime, test_range, gids, rids from history where uid = %s" % st.session_state.user_id
            addquery = ""
            if st.session_state.history_subject:
                addquery = " and test_range like '과목: %s%%' " % st.session_state.history_subject
                if st.session_state.history_part:
                    addquery = " and test_range like '%%파트: %s%%' " % st.session_state.history_part
            db = sqlite3.connect("data.db")
            cu = db.cursor()
            data = []
            cu.execute(query+addquery+" order by day desc, stime desc")
            temp=cu.fetchall()
            db.close()
            for i in temp:
                day = i[0]
                stime = i[1]
                etime = i[2]
                test_range = i[3]
                gids = i[4].split(",")
                rids = i[5].split(",")
                point = int(len(rids) / len(gids) * 100) if rids[0] != '' else 0
                data.append((day, stime, etime, test_range, point))
            st.session_state.history_list = data



    st.divider()
    if st.session_state.history_list:
        data = st.session_state.history_list
        history_range = data[0][-2]
        st.session_state.history_range = history_range
        st.write("문제 출제 범위 - %s" % history_range)
        st.write("총 %s개의 응시내역이 검색됨" % len(data))

        df = pd.DataFrame(data, columns=("날짜", "시작시간", "마감시간", "문제출제 범위", "취득 점수"))
        st.table(df)


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