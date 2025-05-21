import openai

def call_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message['content']

def parse_movie_titles(response_text: str) -> list:
    # 예: GPT가 1. 파묻힌 (Buried) ... 이런 식으로 줄바꿈된 목록일 때 처리
    lines = response_text.strip().split("\n")
    titles = [line.split(". ", 1)[-1].split(" (")[0] for line in lines if line]
    return titles
