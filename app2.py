import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="맞춤 성경 구절 상담실",
        page_icon="📖",
        layout="centered",
    )
except Exception:
    pass

st.title("📖 AI 맞춤 성경 구절 추천 & 신앙 상담")
st.caption(
    "지금 마음의 상태와 고민을 자유롭게 나눠주세요. 성경 66권 말씀 중 성도님의"
    " 마음에 꼭 필요한 성경 구절과 따뜻한 위로를 전해드립니다."
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
            "안녕하세요, 성도님. 마음을 담아 환영합니다. 📖\n\n"
            "살아가다 보면 말로 다 표현하기 힘든 고민과 무게를 느낄 때가"
            " 있습니다.\n"
            "지금 성도님의 마음 상태는 어떠신가요?\n\n"
            "💭 **예시 고민 주제:**\n"
            "- 미래에 대한 불안과 두려움\n"
            "- 인간관계나 가족 문제로 인한 상처\n"
            "- 신앙적 회의감이나 기도의 막힘\n"
            "- 건강, 취업, 재정적인 어려움\n\n"
            "편안하게 성도님의 이야기와 고민을 나눠주시면, 마음에 힘이 되는"
            " 하나님 말씀을 찾아드릴게요."
        ),
    }]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기 및 AI 답변 처리
if user_input := st.chat_input("성도님의 고민이나 마음 상태를 적어주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 고민 상태 맞춤 추천 지시문 (프롬프트)
    prompt = f"""
    너는 성경 전체(구약 39권, 신약 27권)를 바탕으로 성도의 마음 상태를 깊이 진단하고 위로하는 따뜻한 AI 신앙 상담사야.

    성도의 고민 및 현재 마음 상태: {user_input}

    아래 구조와 지침에 맞춰 정성스러운 답변을 작성해줘.

    [답변 구조]
    1. **공감과 위로의 인사**: 성도가 털어놓은 고민과 마음 상태(두려움, 상처, 외로움, 답답함 등)를 성경적이고 따뜻한 목회적 시선으로 깊이 공감해줘.
    2. **맞춤 성경 구절 추천**: 성도의 고민 상태에 가장 직접적인 위로와 소망이 되는 성경 구절 1~2개를 엄선해서 보여줘.
       - 장/절(예: 이사야 41장 10절)과 실제 말씀 본문 전체를 명확하게 적어줄 것.
    3. **말씀 풀이 및 영적 가이드**: 이 말씀이 왜 지금 성도의 고민과 마음 상태에 은혜가 되는지, 삶에서 어떻게 마음을 정돈하면 좋을지 친절하게 풀어 설명해줘.
    4. **짧은 한 줄 기도문**: 성도가 마음으로 따라 기도할 수 있는 따뜻한 1~2줄의 기도문으로 마무리해줘.
    """

    try:
        # 에러 방지를 위한 표준 모델명 사용
        model = genai.GenerativeModel("gemini-1.5-flash")
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
