import re

from frame.ToolBox.ConnectFile import read_config_of_db

# 连接数据库
_db = read_config_of_db()

# 配置路由
URL_CONTENT_DICT = dict()


def route(string):
    '''
    创建路由功能
    :param string: 页面地址
    :return: None
    '''
    def call_func(function):
        URL_CONTENT_DICT[string] = function
    return call_func


@route('/index.html')
def index():
    with open("templates/index.html", encoding='utf-8') as f:
        data = f.read()

    word_content = tuple(_db.select("select * from word_table"))

    html = """"""
    for word_info in word_content:
        html_templates = """
            <tr>
                <th>{}</th>
                <th>{}</th>
    
            </tr>
            <tr>
                <th colspan="2">{}</th>
            </tr>
        """.format(word_info[1], word_info[2], None)

        html += html_templates

        data = re.sub(r"\{%content%\}", str(html), data)
        return data


def application(env, set_header):
    set_header('200 OK', [("Content-Type", "text/html;charset=utf-8")])
    file_name = env['PATH_INFO']
    try:
        return URL_CONTENT_DICT[file_name]()
    except Exception as e:
        return "content error:{}".format(e.args)