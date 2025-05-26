# gpt_client.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 사용자의 취향을 고려해 영화를 추천해주는 친절한 AI입니다.\n"
                    "항상 정확히 3개의 영화를 추천해 주세요.\n"
                    "응답은 반드시 아래와 같은 **JSON 형식**의 배열로만 해 주세요:\n"
                    "[\n  {\n    \"title\": \"...\",\n    \"description\": \"...\",\n    \"tmdb_hint\": \"...\"\n  },\n  { ... },\n  { ... }\n]\n"
                    "설명, 마크다운, 여는 말이나 닫는 말 등은 절대 포함하지 마세요.\n"
                    "반드시 JSON 배열만 출력해 주세요."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
