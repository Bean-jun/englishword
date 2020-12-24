# -*- coding: utf-8 -*-
import hashlib
import urllib.parse
import os
import random
import time
import requests
from lxml import etree


class YouDaoTranslate(object):
    def __init__(self, content):
        self.content = content
        self.url = 'http://m.youdao.com/translate'
        self.audio_url = 'http://dict.youdao.com/dictvoice?audio={}&type=1'.format(self.content)
        self.data = {
            'inputtext': self.content,
            'type': 'AUTO',
            }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    def get_translate_content(self):
        '''获取结果并分析'''
        response = requests.post(
            url=self.url,
            headers=self.headers,
            data=self.data
        )
        html = etree.HTML(response.text)
        translate = html.xpath('//*[@id="translateResult"]/li/text()')[0]
        return translate

    def get_audio_wav_file(self):
        '''获取音频文件'''
        response = requests.get(
            self.audio_url,
            headers=self.headers
        )
        FILE_PATH = "{}/{}.mpeg".format('Media', urllib.parse.quote(self.content))
        with open(FILE_PATH, 'wb') as f:
            f.write(response.content)

    def run(self):
        '''运行程序'''
        t = self.get_translate_content()
        self.get_audio_wav_file()
        print(t + '\n')
        os.system('temp.mpeg')


class BaiDuTranslate(object):
    def __init__(self, *args):
        self.appid = '20200712000518003' # 百度账号ID
        self.secretKey = 'Obubbm26Eq0Itay4NbZ5' # 百度账号秘钥
        self.content = args

    def get_translate_content(self):
        base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        for word in self.content:
            salt = random.randint(32768, 65536)
            sign = self.appid + word + str(salt) + self.secretKey
            sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
            url = base_url + '?appid=' + self.appid + '&q=' + word + '&from=auto&to=zh&salt=' +\
                  str(salt) + '&sign=' + sign
            try:
                response = requests.get(url)
                result_all = response.json()
                result = result_all['trans_result'][0]['dst']
                yield word, result
                time.sleep(1)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print('--结束运行请使用Ctrl+C')
    while True:
        content = input("请输入您要翻译的内容(中英文皆可):\n")
        translater = YouDaoTranslate(content)
        translater.run()
        time.sleep(1.25)
