from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {"role": "user", "content": "OpenAI API를 설명해주세요."}
    ],
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta

    if delta.content:
        print(delta.content, end="")