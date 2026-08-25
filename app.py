// 하루 최대 접수 인원 설정
var MAX_RESPONSES = 50;

// 👉 성도님의 실제 Streamlit 웹앱 주소를 아래 따옴표 안에 넣어주세요!
var STREAMLIT_WEBAPP_URL = "https://your-app-name.streamlit.app";


// [기능 1] 응답 제출 시: 자동 이메일 발송 + 하루 인원 제한 체크
function onFormSubmit(e) {
  var form = FormApp.getActiveForm();
  var responses = form.getResponses();
  
  // 가장 최근 제출된 응답 가져오기
  var latestResponse = responses[responses.length - 1];
  var itemResponses = latestResponse.getItemResponses();
  
  // ----------------------------------------------------
  // 1. 작성한 이메일 주소 및 이름 가져오기
  // (질문 순서: 1번-성함, 2번-이메일)
  // ----------------------------------------------------
  var userName = itemResponses[0].getResponse();  // 1번째 질문 답변 (성함)
  var userEmail = itemResponses[1].getResponse(); // 2번째 질문 답변 (이메일)

  // ----------------------------------------------------
  // 2. 이메일 자동 발송
  // ----------------------------------------------------
  if (userEmail && userEmail.indexOf("@") !== -1) {
    var subject = "[신앙 고민 상담] 상담 신청 확인 및 AI 상담실 안내";
    var body = userName + " 성도님, 안녕하세요.\n\n" +
               "신앙 고민 상담 신청이 정상적으로 접수되었습니다.\n\n" +
               "아래 링크를 클릭하시면 성도님의 고민에 맞는 AI 1:1 고민 상담 및 맞춤 설교 추천을 이용하실 수 있습니다.\n\n" +
               "👉 AI 상담실 바로가기:\n" + STREAMLIT_WEBAPP_URL + "\n\n" +
               "감사합니다. 늘 평안하시기를 기도합니다.";
    
    // 메일 보내기
    GmailApp.sendEmail(userEmail, subject, body);
  }

  // ----------------------------------------------------
  // 3. 오늘 하루 접수 인원 제한 체크 (50명)
  // ----------------------------------------------------
  var today = new Date();
  var todayString = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
  
  var todayCount = 0;
  for (var i = 0; i < responses.length; i++) {
    var respDate = responses[i].getTimestamp();
    var respDateString = respDate.getFullYear() + '-' + (respDate.getMonth() + 1) + '-' + respDate.getDate();
    if (respDateString === todayString) {
      todayCount++;
    }
  }
  
  if (todayCount >= MAX_RESPONSES) {
    form.setAcceptingResponses(false);
    form.setCustomClosedFormMessage("오늘 상담 신청 인원(" + MAX_RESPONSES + "명)이 마감되었습니다. 내일 다시 신청해 주세요!");
  }
}


// [기능 2] 매일 자정에 설문 접수 다시 열기
function resetFormDaily() {
  var form = FormApp.getActiveForm();
  form.setAcceptingResponses(true);
}
