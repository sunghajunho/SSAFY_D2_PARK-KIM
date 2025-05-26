# gpt_client.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 영화 추천을 도와주는 어시스턴트입니다.\n"
                    "먼저, 추천의 이유를 한 문장으로 간단히 요약해 주세요.\n"
                    "그 다음, 아래 형식에 따라 정확히 3개의 영화를 JSON 배열로 출력해 주세요:\n"
                    "[\n  {\n    \"title\": \"영화 제목\",\n    \"description\": \"추천 이유\",\n    \"tmdb_hint\": \"TMDB에서 검색에 사용할 키워드 또는 감독 이름\"\n  },\n  ...\n]\n"
                    "응답은 다음과 같은 JSON 객체여야 합니다:\n"
                    "{\"explanation\": \"요약 문장\", \"recommendations\": [ ... ]}\n"
                    "추가 설명 없이 위 JSON 형식으로만 응답해 주세요."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content