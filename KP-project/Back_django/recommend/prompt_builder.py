def build_prompt(user_input, user=None):
    base = f"'{user_input}'에 어울리는 영화를 3개 추천해줘. JSON 형식으로 다음처럼:"
    sample = """
[
  {
      "title": "영화 제목" 
      "description": "추천 이유",
      "tmdb_hint": "TMDB에서 찾을 수 있는 키워드 또는 감독 이름"
    }
]
"""
    if user:
        base = f"{user}님의 취향을 반영해서, " + base
    return base + sample
