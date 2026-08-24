import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page Config 오류 방지 구문
try:
    st.set_page_config(page_title="인천성산교회 영적 신앙 가이드", icon="⛪")
except Exception:
    pass

st.title("⛪ 인천성산교회 영적 신앙 가이드 챗봇")

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")

# CSV 설교 데이터 로드
@st.cache_data
def load_data():sunsan_data.csv
    return pd.read_csv("설교추천100 - 시트1.csv")

try:
    df = load_data()
except Exception as e:
    st.error("설교 데이터베이스(CSV) 파일을 읽지 못했습니다. GitHub 파일명을 확인해주세요.")
    df = pd.DataFrame()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 성도님의 영적 상태를 점검하고 인천성산교회의 맞춤 설교를 추천해 드립니다.\n\n1. 최근 마음이 가장 힘들거나 무거운 상황은 무엇인가요?\n2. 하나님과의 관계에서 느낀 답답함이 있으신가요?\n3. 신앙의 중심(구원의 확신)이 흔들린 경험이 있나요?\n4. 문제나 상처를 하나님께 맡기고 계신가요?\n5. 지금 가장 회복되고 싶은 은혜의 영역은 무엇인가요?"}
    ]

# 기존 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기
if user_input := st.chat_input("답변이나 신앙 고민을 입력해주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 데이터베이스 텍스트 변환
    db_text = df[['설교 제목', '영상 링크']].to_string() if not df.empty else ""
    
    prompt = f"""
    너는 인천성산교회 영적 신앙 가이드 챗봇이야.
    아래는 인천성산교회 실제 설교 데이터베이스 목록이야:
    {db_text}

    성도의 답변: {user_input}

    위 성도의 고민을 성경적 시선으로 따뜻하게 위로 및 진단하고,
    데이터베이스 목록 안에서 가장 적절한 실제 설교 제목과 영상 링크(URL)를 찾아서 정확히 추천해줘.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            bot_reply = response.text
        else:
            bot_reply = "답변을 생성하지 못했습니다. 다시 입력해주세요."

    except Exception as e:
        bot_reply = f"API 오류가 발생했습니다: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
