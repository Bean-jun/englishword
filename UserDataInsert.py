import hashlib

from GetTranslation import get_translation
from ConnectFile import read_config_of_db


# 连接数据库
_db = read_config_of_db()


class UserDataInsert():
    """
    用户数据插入表

    用户不存在时，自动创建用户，并插入数据表中
    """

    __slots__ = ('_name', '_password', '_flag')
    __object = None

    def __init__(self, name, password):
        self._name = name
        self._password = UserDataInsert.__user_password(password)
        self._flag = bool(
            list(_db.select("""select userid, username from user_table where username='{}' and password='{}';"""
                            .format(self._name, self._password))))
        print("当前用户状态----{}----".format(self._flag))

    def __new__(cls, *args, **kwargs):
        if cls.__object is None:
            cls.__object = super().__new__(cls)
        return cls.__object

    @classmethod
    def __user_password(cls, password):
        '''
        转换用户密码并返回
        :param password: password
        :return: password
        '''
        password = hashlib.md5(str(password).encode('utf-8')).hexdigest()
        return password

    @classmethod
    def __get_word_flag_with_content(cls, content):
        '''
        返回当前单词是否在数据库中，
        存在返回    True,单词id
        不存在返回   False,空列表
        :param content: 单词
        :return: 单词存在状态, 单词id
        '''
        word_id = list(
            _db.select("""select word_id from word_table where word='{}';"""
                      .format(content)))
        word_flag = bool(word_id)
        return word_flag, word_id

    @classmethod
    def __get_user_word_flag(cls, userid, word_id):
        '''
        判断当前用户中是否已经存在过单词
        :param userid: 用户id
        :param word_id: 单词id
        :return: 用户表单词存在状态
        '''
        if bool(list(_db.select("""select word_id from user_word_table where userid={} and word_id={};"""
                               .format(userid, word_id)))):
            return True
        else:
            return False

    def __user_register(self):
        '''
        判断当前用户是否存在表中
        不存在 创建用户
        :return : None
        '''
        if self._flag is False:
            end_user_id = list(_db.select("""select userid from user_table"""))
            end_user_id = [0] if bool(end_user_id) is False else end_user_id[-1]
            fake_user_id = end_user_id[0] + 1
            _db.insert('user_table', userid=fake_user_id, username=self._name, password=self._password)
            self._flag = True

    def __insert_data(self, word_id):
        '''
        插入用户数据
        :param word_id:
        :return:
        '''
        userid = list(_db.select("""select userid from user_table where username='{}' and password='{}';"""
                                .format(self._name, self._password)))[0][0]
        if UserDataInsert.__get_user_word_flag(userid, word_id[0][0]) is False:
            _db.insert("user_word_table", userid=userid, word_id=word_id[0][0], study_count=1)

    def user_data_insert(self, *args):
        '''
        插入用户单词数据
        :param args: 单词元组
        :return: None
        '''
        for word in args:
            word_flag, word_id = UserDataInsert.__get_word_flag_with_content(word)

            if word_flag is True:
                if self._flag is False:
                    self.__user_register()
                self.__insert_data(word_id)

            if word_flag is False:
                if self._flag is False:
                    self.__user_register()
                get_translation(word)
                try:
                    _, word_id = UserDataInsert.__get_word_flag_with_content(word)
                except Exception as e:
                    print(e.args[0], 'this is error in UserDataInsert.user_data_insert')
                self.__insert_data(word_id)


if __name__ == "__main__":
    test = UserDataInsert('小拳拳同学', 123456)
    test.user_data_insert('collection', 'key', 'syntax', 'two', 'bean', 'map', 'invalid', 'key', 'syntax', 'two',
                          'bean', 'map', 'args')
