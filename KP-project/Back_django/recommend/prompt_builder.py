# prompt_builder.py
def build_prompt(user_input, username=None, preferred_genres=None, watch_history=None):
    preferred_genres = preferred_genres or []
    watch_history = watch_history or []

    # 1. 사용자 소개부
    intro = ""
    if username:
        intro += f"{username}님의 취향을 반영해서, "
    if preferred_genres:
        intro += f"선호 장르는 {', '.join(preferred_genres)}입니다. "

    # 2. 기본 요청 문장 (user_input을 핵심으로, 나머지는 참고용으로)
    core = (
        f"'{user_input}'에 어울리는 영화를 추천해줘. "
        "사용자의 선호 장르와 시청 이력도 참고하되, 입력 내용이 가장 중요합니다. "
        "먼저 추천 이유를 한 문장으로 요약하고, "
        "그 다음 3개의 영화를 JSON 배열로 제공해줘.\n"
    )

    # 3. 시청 기록 제외 요청
    exclusion = ""
    if watch_history:
        exclusion = " 이전에 시청한 영화는 추천에서 제외해줘. 예: " + ', '.join(watch_history[:20])

    # 4. JSON 포맷 지시
    format_guide = " 다음 형식의 JSON으로 응답해줘:\n" + (
        """
[
  {
    "title": "영화 제목",
    "description": "추천 이유",
    "tmdb_hint": "TMDB에서 찾을 수 있는 키워드 또는 감독 이름"
  }
]
"""
    )

    return intro + core + exclusion + format_guide
