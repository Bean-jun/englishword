import hashlib

from ContentToDatabase import DatabaseOperate
from GetTranslation import get_translation
from GetResult import get_result

DATE_BASE = './WordLearn.db'
db = DatabaseOperate(DATE_BASE)


class UserDataInsert(object):
    """
    用户数据插入表

    用户不存在时，自动创建用户，并插入数据表中
    """

    __slots__ = ('name', 'password', '_flag')
    __object = None

    def __init__(self, name, password):
        self.name = name
        self.password = UserDataInsert.__user_password(password)
        self._flag = bool(
            list(get_result("""select userid, username from user_table where username='{}' and password='{}';"""
                            .format(self.name, self.password))))
        print("当前用户状态----{}----".format(self._flag))

    def __new__(cls, *args, **kwargs):
        if cls.__object is None:
            cls.__object = super().__new__(cls)
        return cls.__object

    @classmethod
    def __user_password(cls, password):
        password = hashlib.md5(str(password).encode('utf-8')).hexdigest()
        return password

    @classmethod
    def __get_word_flag_with_content(cls, content):
        word_id = list(
            get_result("""select word_id from word_table where word='{}';"""
                       .format(content)))
        word_flag = bool(word_id)
        return word_flag, word_id

    @classmethod
    def __get_user_word_flag(cls, userid, word_id):
        if bool(list(get_result("""select word_id from user_word_table where userid={} and word_id={};"""
                                .format(userid, word_id)))):
            return True
        else:
            return False

    def __user_register(self):
        if self._flag is False:
            end_user_id = list(get_result("""select userid from user_table"""))
            end_user_id = [0] if bool(end_user_id) is False else end_user_id[-1]
            fake_user_id = end_user_id[0] + 1
            db.insert('user_table', userid=fake_user_id, username=self.name, password=self.password)
            self._flag = True

    def __insert_data(self, word_id):
        userid = list(get_result("""select userid from user_table where username='{}' and password='{}';"""
                                 .format(self.name, self.password)))[0][0]
        if UserDataInsert.__get_user_word_flag(userid, word_id[0][0]) is False:
            db.insert("user_word_table", userid=userid, word_id=word_id[0][0], study_count=1)

    def user_data_insert(self, *args):
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
