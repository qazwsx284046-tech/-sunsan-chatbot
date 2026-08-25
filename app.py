import google.generativeai as genai
import pandas as pd
import streamlit as st

# ==========================================
# 0. 구글 설문지 URL 설정
# 1단계에서 만든 구글 설문지의 [보내기] -> [<>] (HTML) 탭에서
# src="..." 안의 주소만 복사하여 아래에 붙여넣어 주세요.
# ==========================================
GOOGLE_FORM_URL = (
    "https://docs.google.com/forms/d/14TkkJdTkB7t_BpgTMuJDFSk6F0GK4tcSkbZLuRVN08s/edit#settings"
)

# Page Config 설정
try:
    st.set_page_config(
        page_title="인천성산교회 영적 신앙 가이드",
        page_icon="⛪",
        layout="centered",
    )
except Exception:
    pass

st.title("⛪ 인천성산교회 영적 신앙 가이드")

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
# CSV 설교 데이터 로드
# ------------------------------------------


@st.cache_data
def load_data():
    return pd.read_csv("sunsan_data.csv")


try:
    df = load_data()
except Exception as e:
    st.error(
        "sunsan_data.csv 파일을 찾을 수 없습니다. GitHub 파일명을 확인해주세요."
    )
    df = pd.DataFrame()

# ------------------------------------------
# 탭(Tab) 구성: 설문지 제출 vs 실시간 AI 상담
# ------------------------------------------
tab1, tab2 = st.tabs(["📋 1. 상담 신청서 작성", "💬 2. 실시간 AI 고민 상담"])

# ------------------------------------------
# [Tab 1] 구글 설문지 임베드 화면
# ------------------------------------------
with tab1:
    st.subheader("📋 신앙 고민 상담 신청서")
    st.caption("하루 선착순 인원 내에서 접수되며, 작성해 주신 내용을 바탕으로 안내해 드립니다.")
    st.markdown("---")

    if "YOUR_FORM_ID" in GOOGLE_FORM_URL:
        st.warning(
            "⚠️ 관리자님! 코드 상단의 `GOOGLE_FORM_URL` 변수에 실제 구글 설문지"
            " 주소를 넣어주세요."
        )
    else:
        # 구글 설문지를 웹앱 내부에 표시
        st.components.v1.iframe(GOOGLE_FORM_URL, height=800, scrolling=True)

# ------------------------------------------
# [Tab 2] Gemini AI 챗봇 화면
# ------------------------------------------
with tab2:
    st.subheader("💬 실시간 AI 신앙 상담 및 설교 추천")
    st.caption("고민을 자유롭게 입력하시면, 따뜻한 위로와 함께 인천성산교회 맞춤 설교를 추천해 드립니다.")

    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": (
                "안녕하세요! 성도님의 영적 상태를 점검하고 인천성산교회의 맞춤"
                " 설교를 추천해 드립니다.\n\n"
                "1. 최근 마음이 가장 힘들거나 무거운 상황은 무엇인가요?\n"
                "2. 하나님과의 관계에서 느낀 답답함이 있으신가요?\n"
                "3. 신앙의 중심(구원의 확신)이 흔들린 경험이 있나요?\n"
                "4. 문제나 상처를 하나님께 맡기고 계신가요?\n"
                "5. 지금 가장 회복되고 싶은 은혜의 영역은 무엇인가요?"
            ),
        }]

    # 기존 대화 내용 출력
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 사용자 입력 받기
    if user_input := st.chat_input("답변이나 신앙 고민을 입력해주세요..."):
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        st.chat_message("user").write(user_input)

        # 데이터베이스 텍스트 변환
        db_text = (
            df[["설교 제목", "영상 링크"]].to_string() if not df.empty else ""
        )

        prompt = f"""
        너는 인천성산교회 영적 신앙 가이드 챗봇이야.
        아래는 인천성산교회 실제 설교 데이터베이스 목록이야:
        {db_text}

        성도의 답변/고민: {user_input}

        위 성도의 고민을 성경적 시선으로 따뜻하게 위로 및 진단하고,
        데이터베이스 목록 안에서 가장 적절한 실제 설교 제목과 영상 링크(URL)를 찾아서 정확히 추천해줘.
        """

        try:
            # 안전하고 최신인 gemini-1.5-flash 모델 사용
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

