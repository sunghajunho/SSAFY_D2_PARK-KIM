import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a movie recommender."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
