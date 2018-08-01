# -*- coding: utf-8 -*-
# 百度ASR调用DEMO

# description:
# author: xiaoland
# create_time: 2018/7/27

"""
    desc:pass
"""

from ASR import BaiduStt

bs = BaiduStt()
token = bs.get_token()    # 获取token

texts = bs.stt_starts('./voice.wav', token) # 实时语音识别，返回为dict{'States': '', 'Text': [word, word, word, word]}
# text = bs.stt_start('./voice.wav', token) # 语音识别

# 对texts（列表）做后续处理，变成完整的句子
text = 'a'
a = 0
i = len(texts['Text'])
while 1 == 1:
    try:
        text = text + texts['Text'][a]
    except IndexError:
        break
    else:
        a += 1
text = text[1:-1]



