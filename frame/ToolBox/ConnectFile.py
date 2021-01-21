import json

from frame.ToolBox.ContentToDatabase import DatabaseOperate


def read_config_of_db():
    with open('./config.conf', 'r', encoding='utf-8') as f:
        config = json.load(f)
    try:
        k = ''
        v = ''
        for database in config['DATABASE'].items():
            if database[1] == 1:
                k = list(config[database[0]].keys())
                v = list(config[database[0]].values())
            if len(v) == 1:
                return DatabaseOperate(v[0])
            elif len(v) > 1:
                kwargs = ["'{}'='{}'".format(k[i], v[i]) for i in range(len(k))]
                kwargs = ','.join(kwargs)
                return DatabaseOperate(kwargs)
    except Exception as e:
        print(e.args[0])


if __name__ == "__main__":
    t = read_config_of_db()
    print(t)