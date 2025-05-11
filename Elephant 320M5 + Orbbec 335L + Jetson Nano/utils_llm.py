# utils_llm.py


print('导入大模型API模块')

import os
import openai
from openai import OpenAI
from API_KEY import *
import qianfan


def llm_qianfan(PROMPT='你好，你是谁？'):
    '''
    百度智能云千帆大模型平台API
    '''

    # 传入 ACCESS_KEY 和 SECRET_KEY
    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY

    # 选择大语言模型
    MODEL = "ERNIE-Bot-4"
    # MODEL = "ERNIE Speed"
    # MODEL = "ERNIE-Lite-8K"
    # MODEL = 'ERNIE-Tiny-8K'

    chat_comp = qianfan.ChatCompletion(model=MODEL)

    # 输入给大模型
    resp = chat_comp.do(
        messages=[{"role": "user", "content": PROMPT}],
        top_p=0.8,
        temperature=0.3,
        penalty_score=1.0
    )

    response = resp["result"]
    return response


def llm_gpt(message):
    # 调用GPT-4 API
    client = OpenAI(api_key='sk-o1s7M1qiqWuKVrSdEb78780d935f4d46Bc6e2b0cA356DeC1',
                    base_url="https://api1.uiuiapi.com/v1/")
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=message)

    # 获取响应结果
    result = completion.choices[0].message.content
    return result

def llm_dpsks(message):
    # 调用GPT-4 API
    client = OpenAI(
        api_key='sk-o8adQPifhKbBRTuYlo40JlSL3U37gf8m4PURfUo5cZjJVTdM',
        base_url="https://api.chatanywhere.tech"
    )
    completion = client.chat.completions.create(model='gpt-4o-2024-11-20', messages=message)

    # 获取响应结果
    result = completion.choices[0].message.content
    return result

def llm_yi(message):
    '''
    零一万物大模型API
    '''

    API_BASE = "https://api.lingyiwanwu.com/v1"
    API_KEY = YI_KEY

    MODEL = 'yi-large'
    # MODEL = 'yi-medium'
    # MODEL = 'yi-spark'

    # 访问大模型API
    client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    # completion = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": PROMPT}])
    # print(message)
    completion = client.chat.completions.create(model=MODEL, messages=message)
    result = completion.choices[0].message.content.strip()
    return result

