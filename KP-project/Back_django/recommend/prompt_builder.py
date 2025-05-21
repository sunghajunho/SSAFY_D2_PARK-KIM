# recommend/prompt_builder.py
def build_prompt(query: str = None, user=None):
    if query:
        return f"""
"{query}"와 어울리는 영화 3편을 추천해줘.
각 영화는 JSON 형식으로 {{ "title": "영화 제목" }} 배열로 반환해줘.
"""
    elif user and user.is_authenticated:
        return f"""
사용자 '{user.username}'의 취향에 맞는 영화를 3편 추천해줘.
각 영화는 {{ "title": "영화 제목" }} 형식의 JSON 배열로 보내줘.
"""
    else:
        return """
최근 인기 있는 영화를 3편 추천해줘.
각 영화는 {{ "title": "영화 제목" }} 형식의 JSON 배열로 보내줘.
"""
