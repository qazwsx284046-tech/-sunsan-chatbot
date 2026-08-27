import google.generativeai as genai
import pandas as pd
import streamlit as st

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
    "성도님의 마음에 필요한 맞춤 성경 구절과 따뜻한 위로를 전해드립니다."
)
st.markdown("---")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에 'GEMINI_API_KEY'를 설정해 주세요.")


@st.cache_data
def load_data():
    return pd.read_csv("bible_data.csv")


try:
    df = load_data()
except Exception:
    df = pd.DataFrame()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "안녕하세요! 성도님을 위한 성경 구절 가이드입니다. 📖\n\n"
            "요즘 마음이 힘들거나 위로받고 싶은 말씀이 있으시다면 편하게"
            " 나누어 주세요."
        ),
    }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("신앙 고민이나 필요한 말씀 주제를 입력해주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    db_text = df.to_string() if not df.empty else ""
    prompt = f"성경 구절 바탕 상담사로서 다음 고민에 맞는 성경 구절과 따뜻한 위로를 전해줘:\n{user_input}\n\n참고 데이터:\n{db_text}"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        bot_reply = (
            response.text
            if response and hasattr(response, "text")
            else "답변 생성 실패"
        )
    except Exception as e:
        bot_reply = f"오류 발생: {str(e)}"

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    st.chat_message("assistant").write(bot_reply)
