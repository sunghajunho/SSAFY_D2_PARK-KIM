export function createPrompt(query) {
  return `
  사용자가 다음과 같은 영화 취향을 입력했습니다: "${query}"

  아래 조건을 참고해서 추천 영화 3개를 JSON 형태로 알려줘.
  각 항목은 아래 형식을 따를 것:

  [
    {
      "title": "영화 제목",
      "description": "추천 이유",
      "tmdb_hint": "TMDB에서 찾을 수 있는 키워드 또는 감독 이름"
    }
  ]
  `;
}

export function createHomePrompt(username = null) {
  if (username) {
    return `사용자 ${username}의 취향을 기반으로 아래 형식의 영화 3개를 추천해줘.
[
  { "title": "Inception", "description": "..." },
  ...
]`
  } else {
    return `최근 화제가 된 대중적인 영화 3개를 아래 형식으로 추천해줘.
[
  { "title": "Oppenheimer", "description": "..." },
  ...
]`
  }
}
