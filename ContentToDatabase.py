# -*- coding: utf-8 -*-
import sqlite3
import logging


class DatabaseOperate(object):
    """
    对数据库的增删改查

    insert：全值插入或缺省值插入
    delete：删除表字段内容
    update：修改表字段内容
    select：查询表内容
    """
    __slots__ = ('db_client', 'cur')
    __object = None
    __fmt = "{asctime},{levelname},{funcName},{message},{process}"
    logging.basicConfig(filename='./.log', filemode='a', level=logging.DEBUG, format=__fmt, style='{')

    def __init__(self, database):
        try:
            db_client = sqlite3.connect(database)
        except Exception as e:
            logging.warning("---->Database Connect Error:{}<----".format(e.args[0]))
        else:
            self.db_client = db_client
            self.cur = self.db_client.cursor()

    def __new__(cls, *args, **kwargs):
        if cls.__object is None:
            cls.__object = super().__new__(cls)
        return cls.__object

    def __del__(self):
        self.cur.close()
        self.db_client.close()

    def __commit(self, field: str, sql):
        try:
            self.cur.execute(sql)
        except Exception as e:
            msg = "{} Error".format(field.title())
            logging.warning("---->{}:\n\t{}\n\t{}<----".format(msg, sql, e.args[0]))
        else:
            self.db_client.commit()

    def insert(self, table, *args, **kwargs):
        if len(args) != 0:
            sql = '''insert into {} values {};'''.format(table, args)
        else:
            sql = '''insert into {} {} values {};'''.format(table, tuple(kwargs.keys()), tuple(kwargs.values()))
        self.__commit('insert', sql)

    def delete(self, table, condition):
        sql = '''delete from {} where {};'''.format(table, str(condition))
        self.__commit('delete', sql)

    def update(self, table, content, condition):
        sql = '''update {} set {} where {};'''.format(table, content, condition)
        self.__commit('update', sql)

    def select(self, sql, size='normal'):
        self.__commit('select', sql)
        if size == 'normal':
            yield from self.cur.fetchall()
        elif size >= 1:
            yield from self.cur.fetchmany(size)


if __name__ == "__main__":
    db = DatabaseOperate('./WordLearn.db')
    db.insert('user_table', userid=20200009, username='小奶狗', user_group='成人', gender='男', tag='游戏中')
    db.insert('user_table', 20200010, '小奶狗', '成人', '男', '游戏中')
    db.delete('user_table', 'userid=20200006')
    db.update('user_table', 'userid=20200002', 'userid=20200001')
    data = db.select('select * from user_table;')
    for result in data:
        print(result)
