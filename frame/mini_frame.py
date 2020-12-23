def index():
    with open("templates/index.html", encoding='utf-8') as f:
        return f.read()


def application(env, set_header):
    set_header('200 OK', [("Content-Type", "text/html;charset=utf-8")])
    file_name = env['PATH_INFO']

    if file_name == "/index.mini":
        print('this is frame')
        return index()
    else:
        return "___mini___frame__404_____"