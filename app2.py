import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="인천성산교회 말씀&타미드 기도 상담실",
        page_icon="📖",
        layout="centered",
    )
except Exception:
    pass

st.title("📖 인천성산교회 AI 말씀 & 타미드 기도 상담실")
st.caption(
    "인천성산교회 주일/강해 말씀 영상, 성경 파노라마(구속사 맥락), 그리고"
    " 아침에 드리는 타미드 기도를 바탕으로 영적 처방전을 드립니다."
)
st.markdown("---")

# =========================================================
# 🎥 인천성산교회 핵심 영성 데이터 (말씀/파노라마/타미드기도)
# (교회 영상 자막이나 설교 스크립트가 있다면 아래에 자유롭게 추가하세요)
# =========================================================
SUNSAN_CORE_DATA = """
[인천성산교회 영성 3대 핵심 기준]

1. 인천성산교회 말씀 영상 영성
- 선포되는 주일 설교 및 강해 말씀을 통해 삶의 현장에 적용하는 실천적 은혜.
- 하나님 중심, 말씀 중심의 영적 회복과 삶의 문제 해결.

2. 인천성산교회 성경 파노라마
- 구약(창세기~말라기)과 신약(마태복음~요한계시록) 전체를 관통하는 구속사적 하나님 나라의 맥락.
- 단편적 구절 해석을 넘어, 창조-타락-구속-완성의 전체 흐름 속에서 성도의 위치를 확인.

3. 인천성산교회 아침에 드리는 타미드 기도
- 매일 아침 하나님 앞에 드리는 상번제(TAMID)의 거룩한 습관.
- 5단계 기도 체계:
  ① 감사와 찬양: 아침을 열며 하나님의 은혜에 감사
  ② 회개와 정돈: 보혈을 의지하여 마음을 정결하게 함
  ③ 말씀 붙들기: 선포된 말씀과 약속의 구절을 심음에 둠
  ④ 간구와 중보: 개인의 고민과 공동체, 가정을 위해 기도
  ⑤ 믿음의 선포: 하루를 승리로 살아가겠다는 담대한 결단
"""

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error(
        "Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. Streamlit 앱"
        " Settings에서 설정해 주세요."
    )

# 대화 기록 초기화 및 첫 인사말
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "샬롬! 인천성산교회 성도님, 환영합니다. 📖\n\n"
            "인천성산교회 **말씀 영상**, **성경 파노라마**, 그리고 **아침에"
            " 드리는 타미드 기도**를 기준으로 성도님의 고민과 마음을"
            " 보듬어 드립니다.\n\n"
            "오늘 마음속 고민이나 나누고 싶은 기도 제목을 편안하게 적어주세요."
        ),
    }]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기 및 AI 답변 처리
user_input = st.chat_input("성도님의 고민이나 기도 제목을 적어주세요...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    prompt = f"""
    너는 인천성산교회의 영성(말씀 영상, 성경 파노라마, 아침에 드리는 타미드 기도)에 깊이 훈련된 따뜻한 AI 신앙 상담사야.
    아래 제공된 [인천성산교회 영성 3대 핵심 기준]을 바탕으로 성도의 고민에 대해 답변해줘.

    [인천성산교회 영성 3대 핵심 기준]
    {SUNSAN_CORE_DATA}

    성도의 고민 및 현재 마음 상태: {user_input}

    [답변 작성 구조]

    1. **목회적 공감과 위로**
       - 인천성산교회 공동체의 시선으로 성도의 마음 고민을 따뜻하게 진단하고 공감해줘.

    2. **성경 파노라마 & 말씀 영상 처방**
       - 구속사적 '성경 파노라마' 흐름과 선포된 말씀 영상의 영적 맥락에서 가장 적합한 성경 구절(장/절 및 본문 전체)을 추천하고, 이 말씀이 성도의 삶에 주는 의미를 풀어줘.

    3. **아침에 드리는 타미드 기도문**
       - 인천성산교회 아침 타미드 기도의 5단계(감사/찬양 -> 회개 -> 말씀붙들기 -> 간구 -> 믿음선포)가 선명하게 녹아든 3~4줄의 아침 맞춤 기도문을 작성해줘.
    """

    try:
        model = genai.GenerativeModel("gemini-3.6-flash")
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            bot_reply = response.text
        else:
            bot_reply = "답변을 생성하지 못했습니다. 다시 입력해주세요."

    except Exception as e:
        bot_reply = f"API 오류가 발생했습니다: {str(e)}"

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    st.chat_message("assistant").write(bot_reply)
