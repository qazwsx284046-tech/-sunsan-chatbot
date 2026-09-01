import datetime
import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="믿음 & 루틴 라이프 노트",
        page_icon="🌿",
        layout="centered",
    )
except Exception:
    pass

st.title("🌿 믿음 & 루틴 라이프 노트")
st.caption(
    "오늘의 말씀 기도, 건강 루틴, 하루 회고를 기록하고 성경파노라마 구속사"
    " 코칭을 받아보세요."
)
st.markdown("---")

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error(
        "Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. Streamlit 앱"
        " Settings에서 설정해 주세요."
    )

# ---------------------------------------------------------
# 1. 기본 정보 & 컨디션
# ---------------------------------------------------------
st.subheader("📌 1. 기본 정보 & 컨디션")
col1, col2 = st.columns(2)
with col1:
    today_date = st.date_input("오늘 날짜", datetime.date.today())
with col2:
    condition_text = st.text_input(
        "오늘의 컨디션 (한 줄)",
        placeholder="예: 아침에 비가 와서 운동하기 귀찮았음",
    )

# ---------------------------------------------------------
# 2. 오늘의 말씀 & 기도문
# ---------------------------------------------------------
st.subheader("📖 2. 오늘의 말씀 & 기도문")
bible_verse = st.text_input(
    "오늘의 성경 구절", placeholder="예: 민수기 14:9"
)
verse_content = st.text_area(
    "구절 본문 또는 설교 요약 메모",
    placeholder=(
        "“여호와는 우리와 함께 하시느니라 그들을 두려워하지 말라.”"
    ),
)
prayer_text = st.text_area(
    "오늘의 기도문 및 묵상 내용",
    placeholder="하나님 아버지, 오늘 하루도...",
    height=150,
)

# ---------------------------------------------------------
# 3. 오늘의 루틴 체크
# ---------------------------------------------------------
st.subheader("✅ 3. 오늘의 루틴 체크")

col_r1, col_r2 = st.columns(2)
with col_r1:
    r_water_morning = st.checkbox("아침 기상 후 미지근한 물 400ml")
    r_water_2l = st.checkbox("하루 물 2L 이상 섭취")
    r_walk_8k = st.checkbox("8,000보 이상 걷기")
    r_sleep = st.checkbox("7~8시간 수면")

with col_r2:
    r_med_before_lunch = st.checkbox("점심 식전 영양제/약 복용")
    r_med_after_lunch = st.checkbox("점심 식후 종합비타민 복용")
    r_ringfit = st.checkbox("링피트/운동 완료 (월/수/금)")

# 상세 세부 수치 기록 (선택)
with st.expander("📊 루틴 세부 수치 기록 (선택사항)"):
    water_amount = st.text_input(
        "물 섭취량 (ml)", placeholder="예: 3000 / 2000"
    )
    walk_count = st.text_input(
        "걸음 수", placeholder="예: 11,578 / 8000"
    )
    sleep_hours = st.text_input(
        "어젯밤 수면시간/기상시간",
        placeholder="예: 10시간 수면, 9시 기상",
    )
    ringfit_detail = st.text_input(
        "링피트 상세 기록", placeholder="예: 20분 / 강도 18 / 120kcal"
    )

# ---------------------------------------------------------
# 4. 하루 회고 (3줄 피드백)
# ---------------------------------------------------------
st.subheader("📝 4. 하루 회고 (3줄 피드백)")
good_point = st.text_area(
    "잘된 점",
    placeholder=(
        "몸이 가볍고 아이디어와 머리가 잘 돌아가고 움직이는 것이 힘들지"
        " 않았음"
    ),
)
bad_point = st.text_area(
    "아쉬운 점",
    placeholder="습하고 더워서 몸이 쳐지고 변화가 눈에 안 보임",
)
tomorrow_goal = st.text_input(
    "내일 실천할 한 가지",
    placeholder="조금 일찍 일어나서 링피트 마무리하고 저녁 7시 전 식사",
)

st.markdown("---")

# ---------------------------------------------------------
# 5. 제출 및 AI 성경파노라마 코칭 리포트
# ---------------------------------------------------------
if st.button("🌿 오늘 일기 제출 & 성경파노라마 코칭 받기"):
    # 입력 데이터 정리
    routines_done = []
    if r_water_morning:
        routines_done.append("아침 물 400ml")
    if r_water_2l:
        routines_done.append(f"물 2L 이상 ({water_amount})")
    if r_walk_8k:
        routines_done.append(f"8,000보 이상 ({walk_count})")
    if r_sleep:
        routines_done.append(f"7~8시간 수면 ({sleep_hours})")
    if r_med_before_lunch:
        routines_done.append("점심 식전 약")
    if r_med_after_lunch:
        routines_done.append("점심 식후 비타민")
    if r_ringfit:
        routines_done.append(f"링피트 운동 ({ringfit_detail})")

    journal_summary = f"""
    [기록 일시]: {today_date}
    [오늘의 컨디션]: {condition_text}
    [성경 구절 및 본문/설교메모]: {bible_verse} - {verse_content}
    [작성한 기도문/묵상]: {prayer_text}
    [달성한 건강 루틴]: {', '.join(routines_done)}
    [잘된 점]: {good_point}
    [아쉬운 점]: {bad_point}
    [내일의 한가지 목표]: {tomorrow_goal}
    """

    st.success("오늘의 루틴 일기가 성공적으로 기록되었습니다! 👏")
    st.text_area(
        "📋 오늘 작성한 일기 요약본", journal_summary, height=180
    )

    # AI 피드백 생성 (오직 창세기~요한계시록 성경파노라마 맥락 기준)
    prompt = f"""
    너는 오직 [창세기부터 요한계시록까지의 성경파노라마 구속사 맥락]에 입각하여 성도를 코칭하는 AI 영성 라이프 코치야.
    성도가 작성한 오늘의 일기와 말씀 메모를 오직 성경 파노라마의 맥락으로만 분석하여 코칭 리포트를 작성해줘.

    [성도가 작성한 오늘의 기록]
    {journal_summary}

    [답변 필수 작성 구조]

    1. 📖 **오늘 말씀의 구속사적 파노라마 요약**
       - 성도가 작성한 말씀({bible_verse})과 설교 메모, 기도 내용을 창세기부터 요한계시록으로 이어지는 전체 구속사 파노라마 흐름 속에서 어떤 위치/의미를 갖는지 2~3줄로 정돈해줘.

    2. 📜 **성경파노라마 연결 구절 처방**
       - 성도가 붙든 말씀과 일맥상통하는 구약/신약 성경파노라마 맥락의 연결 성경 구절 1~2개(권/장/절 및 본문 전체)를 엄선하여 제시해줘.

    3. 🌿 **성경파노라마 기반 영적 코칭**
       - 오늘 성도가 겪은 컨디션, 건강 루틴, 회고 내용(잘된 점/아쉬운 점)을 오직 구속사적 성경파노라마의 관점(예: 광야의 훈련, 성육신의 은혜, 하나님 나라의 소망 등)으로 해석하고, 승리할 수 있는 영적 코칭을 제공해줘.

    4. 🕊️ **구속사적 축복과 선포 (2~3줄)**
       - 하나님의 언약과 완성을 바라보는 구속사적 선포와 축복의 기도문으로 마무리해줘.
    """

    with st.spinner(
        "AI 라이프 코치가 성경파노라마 코칭 리포트를 작성 중입니다..."
    ):
        try:
            model = genai.GenerativeModel("gemini-3.6-flash")
            response = model.generate_content(prompt)

            st.markdown("### 💌 성경파노라마 AI 영성 코칭 리포트")
            if response and hasattr(response, "text"):
                st.info(response.text)
            else:
                st.error("피드백을 생성하지 못했습니다.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
