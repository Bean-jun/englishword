import re
import socket
import gevent
from gevent import monkey
from frame import mini_frame

monkey.patch_all()


class WSGIServer(object):
    def __init__(self, port):
        # 创建套接字
        self.status = None
        self.headers = None
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 创建连接
        self.tcp_socket.bind(("", port))

        # 开始监听
        self.tcp_socket.listen(128)

    def send_server(self, tcp_client):
        recv_data = tcp_client.recv(1024).decode('utf-8')
        recv_data = recv_data.splitlines()

        try:
            ret = re.match("[^/]+(/[^ ]*)", str(recv_data[0]))

            if ret:
                file_name = ret.group(1)
                if file_name == '/':
                    file_name = '/index.html'

            # 让网站支持伪静态，非html通过服务器直接加载
            if not file_name.endswith('.html'):
                try:
                    with open("./static"+file_name, 'rb') as f:
                        body = f.read().decode('utf-8')
                except Exception as e:
                    print(e.args)
                    header = "HTTP/1.1 404 NOT FOUND\r\n"
                    header += "\r\n"
                    body = "_________404____________"

                    response = header + body

                    tcp_client.send(response.encode('utf-8'))
                else:
                    header = "HTTP/1.1 200 OK\r\n"
                    header += "\r\n"

                    response = header + body

                    tcp_client.send(response.encode('utf-8'))
            else:
                env = dict()
                env["PATH_INFO"] = file_name

                body = mini_frame.application(env, self.set_header)

                header = "HTTP/1.1 {}\r\n".format(self.status)
                for temp in self.headers:
                    header += "{}:{}\r\n".format(temp[0], temp[1])
                header += "\r\n"

                response = header + body

                tcp_client.send(response.encode('utf-8'))
        except Exception as e:
            print(e.args)
            header = "HTTP/1.1 404 NOT FOUND\r\n"
            header += "\r\n"
            body = "_________404____________"

            response = header + body

            tcp_client.send(response.encode('utf-8'))

        tcp_client.close()

    def set_header(self, status, headers):
        self.status = status
        self.headers = headers

    def run_server(self):
        while True:
            tcp_client, tcp_addr = self.tcp_socket.accept()

            gevent.spawn(self.send_server, tcp_client)

        self.tcp_socket.close()


def main():
    server = WSGIServer(9999)
    server.run_server()


if __name__ == "__main__":
    main()