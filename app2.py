import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="마음약국 처방전 - 인천성산교회",
        page_icon="💊",
        layout="centered",
    )
except Exception:
    pass

# 메인 타이틀
st.title("💊 마음약국 처방전")
st.caption(
    "창세기부터 요한계시록까지 성경파노라마의 말씀과 타미드(TAMID) 기도"
    " 처방전입니다."
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

# 대화 기록 초기화 및 첫 인사말
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "샬롬! 인천성산교회 **마음약국**입니다. 💊📖\n\n"
            "성도님의 마음 고민이나 기도 제목을 입력해 주세요.\n"
            "창세기부터 요한계시록까지 **성경파노라마 구속사 말씀 중 고민에"
            " 딱 맞는 성경 구절**과 **타미드 기도문**을 처방해 드립니다."
        ),
    }]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기 및 AI 답변 처리
user_input = st.chat_input("마음의 고민 증상이나 기도 제목을 입력하세요...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 성경파노라마 구절 및 타미드 기도 중심 프롬프트
    prompt = f"""
    너는 인천성산교회의 영성 기반 AI 신앙 상담사야.
    성도가 제시한 고민에 맞춰, 창세기부터 요한계시록까지의 [성경파노라마] 흐름 속에서 가장 적합한 성경 구절을 찾아 제공하고, [타미드(TAMID) 기도 처방전]을 작성해줘.

    성도의 마음 고민/상황: {user_input}

    [답변 작성 형식 규칙]
    - 불필요한 긴 해설은 배제하고, 고민에 꼭 맞는 성경 구절 본문을 명확히 보여줄 것.

    [출력 구조]

    🩺 **마음 진단**
    (성도의 고민 상태를 1~2줄로 따뜻하게 공감 및 진단)

    📖 **성경파노라마 말씀 처방 (창세기~요한계시록 구속사 흐름)**
    - **[구절 1]** (예: 창세기 28:15 / 이사야 41:10 / 요한계시록 21:4 등 창세기~요한계시록 중 가장 적절한 성경 구절 장/절과 말씀 본문 전체)
    - **[구절 2]** (상황에 맞게 추가 1개 구절 장/절 및 본문 전체)

    💊 **타미드(TAMID) 기도 처방전**
    (타미드 기도 노트의 감사·회개·말씀입각·간구·선포가 담긴 3~4줄의 기도문)
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
