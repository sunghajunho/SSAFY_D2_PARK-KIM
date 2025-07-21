# gemini_client.py
import os
import google.generativeai as genai
import json

# Gemini API 키 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

def call_gemini(prompt, model_name="gemini-1.5-flash"):
    """
    Gemini API를 사용하여 영화 추천을 생성합니다.
    
    Args:
        prompt (str): 사용자 입력 프롬프트
        model_name (str): 사용할 Gemini 모델명 (기본값: gemini-1.5-flash)
    
    Returns:
        str: JSON 형태의 추천 결과
    """
    
    system_prompt = (
        "당신은 영화 추천을 도와주는 어시스턴트입니다.\n"
        "먼저, 추천의 이유를 한 문장으로 간단히 요약해 주세요.\n"
        "그 다음, 아래 형식에 따라 정확히 3개의 영화를 JSON 배열로 출력해 주세요:\n"
        "[\n  {\n    \"title\": \"영화 제목\",\n    \"description\": \"추천 이유\",\n    \"tmdb_hint\": \"TMDB에서 검색에 사용할 키워드 또는 감독 이름\"\n  },\n  ...\n]\n"
        "응답은 다음과 같은 JSON 객체여야 합니다:\n"
        "{\"explanation\": \"요약 문장\", \"recommendations\": [ ... ]}\n"
        "추가 설명 없이 위 JSON 형식으로만 응답해 주세요."
    )
    
    full_prompt = f"{system_prompt}\n\n사용자 요청: {prompt}"
    
    try:
        response = model.generate_content(full_prompt)
        
        # 응답에서 JSON 부분만 추출
        response_text = response.text.strip()
        
        # JSON 형식이 아닌 경우를 대비한 처리
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
        
        return response_text
        
    except Exception as e:
        print(f"Gemini API 호출 중 오류 발생: {e}")
        return None 