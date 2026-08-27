import google.generativeai as genai
import streamlit as st

# Page Config 설정
try:
    st.set_page_config(
        page_title="마음약국 처방전",
        page_icon="💊",
        layout="centered",
    )
except Exception:
    pass

st.title("💊 마음약국 처방전")
st.caption(
    "창세기부터 요한계시록까지 성경파노라마의 말씀과 타미드(TAMID) 기도"
    " 처방전입니다."
)
st.markdown("---")

# =========================================================
# 📖 창세기~요한계시록 성경파노라마 전체 강의/스크립트 데이터
# (아래 큰따옴표 """ 사이에 영상 원본 자막 및 텍스트 전체를 붙여넣으시면 됩니다)
# =========================================================
PANORAMA_DATA = """
[창세기~요한계시록 성경파노라마 데이터]

1. 창세기~신명기 (모세오경): 창조, 타락, 족장 언약, 출애굽, 광야 훈련 및 율법
2. 여호수아~에스더 (역사서): 가나안 정복, 사사 시대, 왕국 형성과 분열, 포로기와 귀환
3. 욥기~아가 (시가서): 고난 속의 찬양, 지혜, 하나님과의 사랑과 경배
4. 이사야~말라기 (선지서): 메시아 예언, 회개의 촉구, 심판과 회복의 소망
5. 마태복음~요한복음 (복음서): 예수 그리스도의 성육신, 십자가 구원과 부활
6. 사도행전 (역사서): 성령의 임재, 교회의 탄생과 복음의 확장
7. 로마서~유다서 (서신서): 성도의 영적 정체성, 교리, 삶의 실천과 영적 전쟁
8. 요한계시록 (예언서): 최종 승리, 새 하늘과 새 땅, 영원한 하나님 나라의 완성

(※ 준비되신 전체 스크립트나 강의안을 여기에 계속 덧붙여 넣으시면 됩니다.)
"""

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error(
        "Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. Streamlit 앱"
        " Settings에서 설정해 주세요."
    )

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "샬롬! **마음약국**입니다. 💊📖\n\n"
            "성도님의 마음 고민이나 기도 제목을 입력해 주세요.\n"
            "창세기부터 요한계시록까지 **성경파노라마 강의 전체 데이터** 기반의"
            " 맞춤 성경 구절과 **타미드 기도문**을 처방해 드립니다."
        ),
    }]

# 기존 대화 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기 및 AI 답변 처리
user_input = st.chat_input("마음의 고민 증상이나 기도 제목을 입력하세요...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    prompt = f"""
    너는 따뜻한 AI 영적 신앙 상담사야.
    아래 제공된 [성경파노라마 전체 데이터]를 바탕으로, 성도의 고민에 가장 직접적으로 부합하는 구속사적 파트와 성경 구절을 추출해줘. 그리고 [타미드(TAMID) 기도 처방전]을 작성해줘.

    [성경파노라마 전체 데이터]
    {PANORAMA_DATA}

    성도의 마음 고민/상황: {user_input}

    [출력 구조]

    🩺 **마음 진단**
    (성도의 고민 상태를 1~2줄로 따뜻하게 공감 및 진단)

    📖 **성경파노라마 말씀 처방 (창세기~요한계시록)**
    - **[관련 파노라마]**: (전체 파노라마 중 해당되는 시대/권역 명시)
    - **[구절 및 본문]**: (성경 구절 장/절과 말씀 본문 전체)

    💊 **타미드(TAMID) 기도 처방전**
    (감사·회개·말씀입각·간구·선포가 담긴 3~4줄의 기도문)
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
