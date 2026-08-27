import google.generativeai as genai
import pandas as pd
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="성경 구절 추천 상담실",
        page_icon="📖",
        layout="centered",
    )
except Exception:
    pass

st.title("📖 AI 성경 구절 추천 및 신앙 상담")
st.caption(
    "신청서를 작성해 주셔서 감사합니다. 지금 성도님의 마음에 필요한"
    " 맞춤 성경 구절과 따뜻한 위로를 전해드립니다."
)
st.markdown("---")

# ------------------------------------------
# API 키 설정
# ------------------------------------------
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error(
        "Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. .streamlit/secrets.toml을"
        " 확인해 주세요."
    )

# ------------------------------------------
# CSV 성경 구절 데이터 로드
# ------------------------------------------


@st.cache_data
def load_data():
    return pd.read_csv("bible_data.csv")


try:
    df = load_data()
except Exception as e:
    st.error(
        "bible_data.csv 파일을 찾을 수 없습니다. GitHub 파일명을 확인해주세요."
    )
    df = pd.DataFrame()

# ------------------------------------------
# 대화 기록 초기화
# ------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "안녕하세요! 성도님을 위한 성경 구절 가이드입니다. 📖\n\n"
            "요즘 마음이 많이 힘들거나, 하나님의 말씀으로 위로받고 싶은"
            " 상황이 있으시다면 편하게 나누어 주세요."
        ),
    }]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ------------------------------------------
# 사용자 입력 받기 및 AI 답변 처리
# ------------------------------------------
if user_input := st.chat_input("신앙 고민이나 필요한 말씀 주제를 입력해주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 데이터베이스 텍스트 변환
    db_text = df.to_string() if not df.empty else ""

    prompt = f"""
    너는 성경 구절을 바탕으로 위로와 가이드를 전하는 AI 신앙 상담사야.
    아래는 참고할 수 있는 추천 성경 구절 목록이야:
    {db_text}

    성도의 고민/상황: {user_input}

    1. 성도의 고민에 대해 성경적이고 따뜻한 시선으로 깊이 위로해줘.
    2. 데이터베이스 목록 및 관련 성경 말씀 중에서 성도에게 가장 힘이 될 성경 구절(구절 이름과 전체 말씀 내용)을 정확히 인용해줘.
    3. 이 말씀이 성도의 상황에 왜 소중한 은혜가 되는지 간단히 풀어 설명해줘.
    """

    try:
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
