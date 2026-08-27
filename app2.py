import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="인천성산교회 맞춤 말씀&기도 상담실",
        page_icon="📖",
        layout="centered",
    )
except Exception:
    pass

st.title("📖 인천성산교회 AI 말씀 & 타미드 기도 상담실")
st.caption(
    "성도님의 고민과 마음 상태를 나눠주세요. 성경 파노라마 관점의 말씀과"
    " 타미드(TAMID) 노트 기반의 영적 가이드 및 기도문을 작성해 드립니다."
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
            "샬롬! 인천성산교회 성도님, 마음을 담아 환영합니다. 📖\n\n"
            "삶의 여러 고민과 기도 제목을 편안하게 나눠주세요.\n"
            "성경 파노라마를 통한 하나님의 구속사적 말씀과 **타미드(TAMID)"
            " 노트** 기준의 영적 가이드 및 기도문을 전해드립니다.\n\n"
            "💭 **예시 고민:** 미래의 두려움, 인간관계 상처, 신앙적 낙심,"
            " 가정/영적 문제 등"
        ),
    }]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기 및 AI 답변 처리
if user_input := st.chat_input("성도님의 고민이나 기도 제목을 적어주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_content := user_input})
    st.chat_message("user").write(user_input)

    # 인천성산교회 타미드 노트 & 성경 파노라마 맞춤 프롬프트
    prompt = f"""
    너는 인천성산교회의 영성과 목회 방향에 깊이 훈련된 따뜻한 AI 신앙 상담사야.
    성도의 고민과 마음 상태를 듣고, 인천성산교회의 [성경 파노라마] 관점과 [타미드(TAMID) 노트] 기도 체계를 적용하여 정성껏 답변해줘.

    성도의 고민 및 현재 마음 상태: {user_input}

    [답변 필수 작성 구조]

    1. **목회적 공감과 위로**
       - 성도의 마음 상태와 고민을 따뜻한 성산교회 공동체의 시선으로 깊이 공감해줘.

    2. **인천성산교회 성경 파노라마 말씀 추천**
       - 구약과 신약 전체를 꿰뚫는 '성경 파노라마' 구속사적 관점에서 성도의 고민에 가장 적합한 성경 구절(장/절 및 본문 전체)을 추천해줘.
       - 이 말씀이 성경 전체 맥락(구속사와 하나님의 언약)에서 어떤 영적 의미를 갖는지 연결하여 설명해줘.

    3. **타미드(TAMID) 노트 기준 영적 가이드**
       - 매일 하나님 앞에 나아가는 매일의 상번제, '타미드(TAMID)' 영성에 맞춘 영적 지침을 제공해줘.
       - 고민 해결을 위한 영적 묵상 포인트와 결단할 실행 조언을 제시해줘.

    4. **타미드(TAMID) 노트 기반 기도문**
       - 타미드 기도 노트의 핵심 요소(감사/찬양 -> 회개 -> 말씀 붙들기 -> 중보/간구 -> 선포/다짐)가 자연스럽게 녹아든 깊이 있는 기도문을 3~4줄로 작성해줘.
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
