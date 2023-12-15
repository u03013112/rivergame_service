import os
import openai

import sys
sys.path.append('/src')

from config import openaiApiKey,openaiUrl

openai.api_type = "azure"
openai.base_url = openaiUrl
openai.api_version = "2023-07-01-preview"
openai.api_key = openaiApiKey

def getAiResp(message_text):
    completion = openai.chat.completions.create(
        model="bigpt4",
        messages=message_text,
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return(completion.choices[0].message.content)


if __name__ == '__main__':
    message = [
        {"role":"system","content":"You are an AI assistant that helps people find information."},
        {"role":"user","content":"你好"}
    ]
    print(getAiResp(message))