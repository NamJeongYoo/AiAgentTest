from openai import OpenAI

# OpenAI 클라이언트 생성
client = OpenAI()

# 모델 호출
response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {"role": "system", "content": "당신은 친절한 AI 비서입니다."},
        {"role": "user", "content": "안녕하세요! 대한민국은 어떠한 나라입니까?"}
    ]
)

# 결과 출력
print(response.choices[0].message.content)