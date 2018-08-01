# -*- coding: utf-8 -*-
# 百度ASR

# description:
# author: xiaoland
# create_time: 2018/7/27

"""
    desc:pass
"""

import sys
import requests
import os
import json
import wave
import pyaudio
import time
import os.path
import demjson
import base64
import urllib
import urllib2
import setting

domian = 'a'


class BaiduStt(object):

    def __init__(self):

        self.set = setting.setting()

    def get_token(self):

        """
        获取token
        :return:
        """

        AK = self.set['ASR']['Baidu']['AK']
        SK = self.set['ASR']['Baidu']['SK']
        url = 'http://openapi.baidu.com/oauth/2.0/token'
        params = urllib.urlencode({'grant_type': 'client_credentials',
                                   'client_id': AK,
                                   'client_secret': SK})
        r = requests.get(url, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)
            return token

    def stt_start(self, fp, token):

        """
        百度语音识别
        :param fp: 文件路径
        :param token: token
        :return:
        """
        try:
            wav_file = wave.open(fp, 'rb')
        except IOError:
            return []
        n_frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        audio = wav_file.readframes(n_frames)
        base_data = base64.b64encode(audio)
        lang = self.set['lang']
        if lang == 'En':
            dev_id = 1737
        elif lang == 'Zh-Hans':
            dev_id = 1936
        elif lang == 'Zh-Yue':
            dev_id = 1637
        elif lang == 'Zh-Chun':
            dev_id = 1837
        else:
            dev_id = 1536
        dataf = {"format": "wav",
                 "token": token,
                 "len": len(audio),
                 "rate": frame_rate,
                 "speech": base_data,
                 "dev_pid": dev_id,
                 "cuid": 'b0-10-41-92-84-4d',
                 "channel": 1}

        data = demjson.encode(dataf)

        r = requests.post('http://vop.baidu.com/server_api',
                          data=data,
                          headers={'content-type': 'application/json'})

        try:
            r.raise_for_status()
            text = ''
            if 'result' in r.json():
                text = r.json()['result'][0].encode('utf-8')
                return {'States': 'BaiduSTTComplete', 'Text': text}
        except requests.exceptions.HTTPError:
            print('Request failed with response: %r',
                  r.text)
            return {'States': 'BaiduSTTError:Request failed with response'}
        except requests.exceptions.RequestException:
            print('Request failed.')
            return {'States': 'BaiduSTTError:Request failed.'}
        except ValueError as e:
            print('Cannot parse response: %s',
                  e.args[0])
            return {'States': 'BaiduSTTError:Request failed.'}
        except KeyError:
            print('Cannot parse response')
            return {'States': 'BaiduSTTError:Cannot parse response'}
        else:
            transcribed = []
            if text:
                transcribed.append(text.upper())
            print(json)

    def stt_starts(self, fn, token):

        """
        百度实时语音识别
        :param fn: 文件路径
        :param token: token
        :return:
        """
        texts = []
        lang = self.set['main_setting']['sys_lang']
        if lang == 'En':
            dev_id = 1737
        elif lang == 'Zh-Hans':
            dev_id = 1936
        elif lang == 'Zh-Yue':
            dev_id = 1637
        elif lang == 'Zh-Chun':
            dev_id = 1837
        else:
            dev_id = 1536

        f = open(fn, 'rb')
        file_content = len(f.read())
        a = 0
        for long in file_content:
            if long % 1024 == 0:
                times = 1
                timess = int(long) / 1024
                while 1 == 1:

                    if times == timess + 1:
                        info = {'States': 'BaiduSttComplete', 'Text': texts}
                        break
                    else:
                        file = f.read()
                        file = file[a:times * 1024]
                        base_data = base64.b64encode(file)

                        dataf = {"format": "wav",
                                 "token": token,
                                 "len": len(audio),
                                 "rate": frame_rate,
                                 "speech": base_data,
                                 "dev_pid": dev_id,
                                 "cuid": 'b0-10-41-92-84-4d',
                                 "channel": 1}

                        data = demjson.encode(dataf)

                        r = requests.post('http://vop.baidu.com/server_api',
                                          data=data,
                                          headers={'content-type': 'application/json'})

                        try:
                            if 'result' in r.json():
                                text = r.json()['result'][0].encode('utf-8')
                                if text == None:
                                    texts.append('')
                                else:
                                    texts.append(text)
                                if a == 0:
                                    a = 1024
                                else:
                                    a = times * 1024
                                times += 1
                            else:
                                info = {'States': 'Error:ResultUnfound', 'Text': None}
                                break
                        except requests.exceptions.HTTPError:
                            print('Request failed with response: %r',
                                  r.text)
                            info = {'States': 'BaiduSTTError:Request failed with response', 'Text': None}
                            break
                        except requests.exceptions.RequestException:
                            print('Request failed.')
                            info = {'States': 'BaiduSTTError:Request failed.', 'Text': None}
                            break
                        except KeyError:
                            print('Cannot parse response')
                            info = {'States': 'BaiduSTTError:Cannot parse response', 'Text': None}
                            break
                break
            else:
                times = 1
                timess = long / 1024 - long // 1024
                while 1 == 1:

                    if times == timess + 1:
                        file = f.read()
                        file = file[a:times * 1024]
                        base_data = base64.b64encode(file)

                        dataf = {"format": "wav",
                                 "token": token,
                                 "len": len(audio),
                                 "rate": frame_rate,
                                 "speech": base_data,
                                 "dev_pid": dev_id,
                                 "cuid": 'b0-10-41-92-84-4d',
                                 "channel": 1}

                        data = demjson.encode(dataf)

                        r = requests.post('http://vop.baidu.com/server_api',
                                          data=data,
                                          headers={'content-type': 'application/json'})

                        try:
                            if 'result' in r.json():
                                text = r.json()['result'][0].encode('utf-8')
                                if text == None:
                                    texts.append('')
                                else:
                                    texts.append(text)
                                if a == 0:
                                    a = 1024
                                else:
                                    a = times * 1024
                                times += 1

                            else:
                                info = {'States': 'Error:ResultUnfound', 'Text': None}
                                break
                        except requests.exceptions.HTTPError:
                            print('Request failed with response: %r',
                                  r.text)
                            info = {'States': 'BaiduSTTError:Request failed with response', 'Text': None}
                            break
                        except requests.exceptions.RequestException:
                            print('Request failed.')
                            info = {'States': 'BaiduSTTError:Request failed.', 'Text': None}
                            break
                        except KeyError:
                            print('Cannot parse response')
                            info = {'States': 'BaiduSTTError:Cannot parse response', 'Text': None}
                            break
                        info = {'States': 'BaiduSttComplete', 'Text': texts}
                        break
                    else:
                        file = f.read()
                        file = file[a:times * 1024]
                        base_data = base64.b64encode(file)

                        dataf = {"format": "wav",
                                 "token": token,
                                 "len": len(audio),
                                 "rate": frame_rate,
                                 "speech": base_data,
                                 "dev_pid": dev_id,
                                 "cuid": 'b0-10-41-92-84-4d',
                                 "channel": 1}

                        data = demjson.encode(dataf)

                        r = requests.post('http://vop.baidu.com/server_api',
                                          data=data,
                                          headers={'content-type': 'application/json'})

                        try:
                            if 'result' in r.json():
                                text = r.json()['result'][0].encode('utf-8')
                                if text == None:
                                    texts.append('')
                                else:
                                    texts.append(text)
                                if a == 0:
                                    a = 1024
                                else:
                                    a = times * 1024
                                times += 1
                            else:
                                info = {'States': 'Error:ResultUnfound', 'Text': None}
                                break
                        except requests.exceptions.HTTPError:
                            print('Request failed with response: %r',
                                  r.text)
                            info = {'States': 'BaiduSTTError:Request failed with response', 'Text': None}
                            break
                        except requests.exceptions.RequestException:
                            print('Request failed.')
                            info = {'States': 'BaiduSTTError:Request failed.', 'Text': None}
                            break
                        except KeyError:
                            print('Cannot parse response')
                            info = {'States': 'BaiduSTTError:Cannot parse response', 'Text': None}
                            break
                break
        f.close()
        return info