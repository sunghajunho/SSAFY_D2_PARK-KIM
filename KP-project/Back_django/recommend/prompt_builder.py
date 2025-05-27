def build_prompt(user_input, username=None, preferred_genres=None, watch_history=None):
    preferred_genres = preferred_genres or []
    watch_history = watch_history or []

    # 1. 사용자 소개부
    intro = ""
    if username:
        intro += f"{username}님의 취향을 반영한 영화를 추천받고 싶습니다. "
    
    genre_prefer = ""
    if preferred_genres:
        genre_prefer = f"사용자의 선호 장르는 {', '.join(preferred_genres)}입니다. "

    # 2. 핵심 요청문
    if user_input and user_input.strip():
        core_input = f"사용자의 입력 조건은 다음과 같습니다: {user_input.strip()} "
    else:
        core_input = "사용자가 검색어는 입력하지 않았고, 기분/상황/장르만 선택하였습니다. 해당 조건을 기반으로 영화를 추천해주세요. "

    core = (
        core_input +
        "입력 조건이 명확한 경우 이를 우선 반영하고, 조건이 모호하거나 비어 있다면 사용자의 선호 장르를 참고해주세요. " +
        "먼저 추천 이유를 한 문장으로 요약한 뒤, 그에 기반한 영화 추천을 JSON 배열로 제공 바랍니다.\n"
    )

    # 3. 시청 기록 제외
    exclusion = ""
    if watch_history:
        exclusion = (
            "다음은 사용자가 이미 시청한 영화 목록입니다. 이들 작품은 추천에서 제외해주세요: "
            + "[" + ', '.join(watch_history[:20]) + "]\n"
        )

    # 4. 포맷 안내
    format_guide = "JSON 응답 양식은 다음과 같습니다:" + (
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

    return intro + core + genre_prefer + exclusion + format_guide
