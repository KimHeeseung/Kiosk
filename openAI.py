import openai

openai.api_key = "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"


# ChatGPT 생성
model_engine = "text-davinci-002"
#model_engine = "curie"
#model_engine = "babbage"
prompt = "mysql 데이터를 특정 조건으로 업데이트하는 파이썬 코드를 알려줘."
completions = openai.Completion.create(
            engine=model_engine,
                prompt=prompt,
                    max_tokens=50
                    )

message = completions.choices[0].text.strip()
print(message)
