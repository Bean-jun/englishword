# -*- coding: utf-8 -*-
import time
import random
import urllib.parse

from GetResult import get_result
from TranslationPack import YouDaoTranslate, BaiDuTranslate
from ContentToDatabase import DatabaseOperate


def get_translation(*args):
    DATE_BASE = './WordLearn.db'
    db = DatabaseOperate(DATE_BASE)
    for word in args:
        tag = random.uniform(0, 2)
        try:
            word_to_num = ord(word[0])
            flag = tag <= 0.5 and 65 < word_to_num < 122

            # 判断当前单词是否存在数据库中,get_download_flag为False则表明不存在
            get_download_flag = bool(list(get_result("""select word from word_table where word='{}'""".format(word))))

            if get_download_flag is False:

                FILE_PATH = "{}/{}.mpeg".format('./Media', urllib.parse.quote(word))

                if flag is True:
                    time.sleep(1)
                    translate = YouDaoTranslate(word).get_translate_content()
                    db.insert('word_table', word=word, word_translate=translate, word_sound=FILE_PATH)
                else:
                    translate = BaiDuTranslate(word).get_translate_content()
                    for _, trans in translate:
                        db.insert('word_table', word=word, word_translate=trans, word_sound=FILE_PATH)

                YouDaoTranslate(word).get_audio_wav_file()

        except Exception as e:
            print(e.args[0], 'this is error in get_translation')

    
if __name__ == "__main__":
    t1 = time.time()
    get_translation('exception', 'content', 'constraint', 'invalid', 'plugin', 'ten', 'readme')
    print(time.time()-t1)