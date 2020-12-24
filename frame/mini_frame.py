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


@route('/index.mini')
def index():
    with open("templates/index.html", encoding='utf-8') as f:
        return f.read()


def application(env, set_header):
    set_header('200 OK', [("Content-Type", "text/html;charset=utf-8")])
    file_name = env['PATH_INFO']
    try:
        return URL_CONTENT_DICT[file_name]()
    except Exception as e:
        return "content error:{}".format(e.args)