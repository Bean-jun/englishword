from frame.ToolBox.ContentToDatabase import DatabaseOperate


def get_result(*args):
    db = DatabaseOperate('./WordLearn.db')
    for sql in args:
        yield from db.select(sql)


if __name__ == "__main__":
    data = get_result('select * from word_table;', 'select * from user_table;', 'select * from user_word_table;')
    for result in data:
        print(result)
