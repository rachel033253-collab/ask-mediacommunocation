import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from datetime import datetime
import io

# --- 페르소나 및 시스템 프롬프트 정의 ---
# 챗봇의 역할과 응대 규칙을 상세하게 정의합니다.
SYSTEM_PROMPT = """
당신은 [미디어커뮤니케이션학과] 학사 정보 Q&A 챗봇입니다. 
사용자는 학과 학생이며, 졸업 요건, 교과목, 장학금, 교수님 정보 등에 대해 질문합니다. 
항상 친절하고 명확하게, 마치 든든한 학과 선배나 조교처럼 답변해야 합니다.

[응대 원칙]
1.  **일반 질문**: 사용자의 질문(예: '졸업학점 몇 점이에요?', '필수과목 뭐예요?')에 대해 당신이 아는 선에서 최선을 다해 답변하세요.
2.  **답변 불가 질문 (민감 정보 또는 복잡한 행정)**: 
    -   만약 질문이 학생 개인의 성적, 수강 내역 등 민감한 개인정보를 요구하거나, 챗봇이 답변할 수 없는 매우 복잡한 행정 절차(예: '저 휴학했는데 군입대 휴학으로 바꿀 수 있나요?')일 경우, 답변이 어렵다고 솔직하게 말해야 합니다.
    -   이 경우, 반드시 다음 절차를 따르세요.
    
[답변 불가 시 응대 절차]
1.  **학과 사무실 안내**: "해당 내용은 학과 사무실의 확인이 필요합니다."라고 먼저 안내합니다.
2.  **질문 요약 및 전달 의사 확인**: 사용자의 질문(무엇이 궁금한지, 어떤 상황인지)을 명확하게 요약한 뒤, "이 내용을 학과 사무실에 전달해 드릴까요?"라고 물어보세요.
3.  **사용자가 전달을 원할 경우**: "정확한 확인 및 회신을 위해 학번과 이메일 주소를 알려주시겠어요?"라고 요청하세요.
4.  **사용자가 연락처 제공을 원치 않을 경우**: "알겠습니다. 다만, 연락처 정보가 없어 학과 사무실의 검토 내용을 회신해 드리기 어려운 점 양해 부탁드립니다."라고 정중히 안내하세요.
"""

# --- 1. API 키 설정 ---
def get_api_key():
    """
    Streamlit secrets에서 API 키를 가져오거나, 없는 경우 사용자 입력을 받습니다.
    """
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
    else:
        st.sidebar.warning("API 키가 설정되지 않았습니다. 임시 키를 입력해주세요.")
        api_key = st.sidebar.text_input("Gemini API Key:", type="password", key="temp_api_key_input")
    
    if not api_key:
        st.error("Gemini API 키가 필요합니다. 사이드바에서 키를 입력해주세요.")
        st.stop()
    return api_key

# --- 2. 세션 초기화 ---
def initialize_session(model):
    """
    Streamlit 세션 상태를 초기화합니다.
    """
    if "chat_session" not in st.session_state:
        # Gemini 모델 채팅 세션 시작
        st.session_state.chat_session = model.start_chat(history=[])
    
    if "messages" not in st.session_state:
        # 화면에 표시될 대화 내역 (Gemini API 형식)
        st.session_state.messages = []
        # 초기 인사 메시지 추가
        st.session_state.messages.append(
            {"role": "model", "parts": ["안녕하세요! 미디어커뮤니케이션학과 챗봇입니다. 무엇을 도와드릴까요?"]}
        )

    if "log" not in st.session_state:
        # CSV 저장을 위한 전체 대화 로그
        st.session_state.log = []

    if "session_id" not in st.session_state:
        # 세션 ID (로그 구분을 위해)
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# --- 3. 대화 기록 함수 ---
def log_message(role, message, log_enabled):
    """
    대화 내용을 st.session_state.log에 기록합니다.
    """
    if log_enabled:
        st.session_state.log.append({
            "timestamp": datetime.now().isoformat(),
            "session_id": st.session_state.session_id,
            "role": role,
            "message": message
        })

# --- 4. 메인 실행 함수 ---
def main():
    st.set_page_config(
        page_title="미컴과 학사 Q&A 챗봇",
        page_icon="🎓",
        layout="centered"
    )

    # 1. API 키 설정
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"API 키 설정 중 오류가 발생했습니다: {e}")
        st.stop()

    # 2. 모델 및 세션 초기화
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        initialize_session(model)
    except Exception as e:
        st.error(f"모델 로딩 중 오류가 발생했습니다: {e}")
        st.stop()

    # 3. 사이드바 (설정 및 제어)
    with st.sidebar:
        st.title("챗봇 제어판")
        
        # 대화 초기화
        if st.button("대화 초기화", key="reset_chat"):
            # 세션 상태의 주요 항목을 초기화
            st.session_state.chat_session = model.start_chat(history=[])
            st.session_state.messages = [
                {"role": "model", "parts": ["대화가 초기화되었습니다. 무엇이 궁금하신가요?"]}
            ]
            # 로그는 유지하되, 새 세션 ID로 구분
            st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.rerun()

        st.divider()

        # 로그 기록 설정
        log_enabled = st.checkbox("대화 자동 기록 (CSV용)", value=True, key="log_toggle")

        # 로그 다운로드
        if st.session_state.log:
            try:
                df = pd.DataFrame(st.session_state.log)
                # UTF-8-SIG로 인코딩하여 Excel에서 한글 깨짐 방지
                csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="대화 로그 다운로드 (.csv)",
                    data=csv_data,
                    file_name=f"chat_log_{st.session_state.session_id}.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"로그 파일 생성 중 오류: {e}")
        
        st.divider()
        
        # 모델 및 세션 정보 표시
        st.info(f"**Model:** gemini-1.5-flash-latest\n\n"
                f"**Session:** {st.session_state.session_id}")

    # 4. 메인 챗 인터페이스
    st.title("미디어커뮤니케이션학과 Q&A 챗봇 🎓")
    st.caption("여러분의 든든한 학과 선배/조교가 되어줄 AI 챗봇입니다.")

    # 4-1. 이전 대화 내역 표시
    for message in st.session_state.messages:
        role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(role):
            st.markdown(message["parts"][0])

    # 4-2. 사용자 입력 처리
    if prompt := st.chat_input("졸업 요건, 장학금 등 궁금한 점을 물어보세요."):
        # 사용자 메시지 표시 및 기록
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        log_message("user", prompt, log_enabled)

        # 4-3. API 컨텍스트 관리 (요청: 최근 6턴)
        # Gemini ChatSession은 내부적으로 히스토리를 관리합니다.
        # 만약 6턴(user 3, model 3)을 초과하면, 세션을 마지막 6개 메시지로 재시작합니다.
        # (참고: messages 리스트에는 초기 인사말이 포함될 수 있으므로 chat_session.history를 기준)
        if len(st.session_state.chat_session.history) > 6:
            try:
                # 마지막 6개 턴으로 히스토리 축소하여 세션 재시작
                st.session_state.chat_session = model.start_chat(
                    history=st.session_state.chat_session.history[-6:]
                )
                print(f"Context truncated. History length: {len(st.session_state.chat_session.history)}")
            except Exception as e:
                st.warning(f"히스토리 재시작 중 오류: {e}")

        # 4-4. Gemini API 호출
        try:
            with st.chat_message("assistant"):
                with st.spinner("답변을 생각 중이에요..."):
                    # ChatSession을 통해 메시지 전송
                    response = st.session_state.chat_session.send_message(prompt)
                    response_text = response.text
            
            # 모델 응답 표시 및 기록
            st.session_state.messages.append({"role": "model", "parts": [response_text]})
            log_message("model", response_text, log_enabled)
            
            # 화면을 즉시 새로고침하여 모델의 마지막 답변을 표시
            st.rerun()

        except genai.types.StopCandidateException as e:
            st.error(f"답변 생성 중지됨: {e}")
            log_message("system_error", f"StopCandidateException: {e}", log_enabled)
        except genai.types.BrokenResponseError as e:
            st.error(f"API 응답 오류: {e}")
            log_message("system_error", f"BrokenResponseError: {e}", log_enabled)
        except Exception as e:
            # 429 (Resource Exhausted) 에러 등 일반적인 API 예외 처리
            st.error(f"메시지 전송 중 오류가 발생했습니다: {e}")
            log_message("system_error", f"Exception: {e}", log_enabled)
            # 429 에러의 경우, Streamlit이 자동으로 재시도하지 않으므로 
            # 사용자에게 잠시 후 다시 시도하라고 안내하는 것이 좋습니다.
            if "429" in str(e):
                st.warning("요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")


# --- 스크립트 실행 ---
if __name__ == "__main__":
    main()
