from openai import OpenAI
from config import config
from llm import chat, stream_parser

system_prompt = config.SYSTEM_PROMPT

def chat(user_prompt, model, max_token=200, temp=0.7):
    client = OpenAI(api_key=config.OPENAI_API_KEY)  # Ensure correct API key is used
    
    completion = client.Completion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temp,
        max_tokens=max_token,
        stream=True  # Ensure the stream parameter is used correctly
    )
    
    return completion

def stream_parse(stream):
    for chunk in stream:
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
