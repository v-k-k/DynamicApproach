from collections.abc import Iterable
from views import index, endpoint
from director import Execute
from loguru import logger
import selectors
import socket
import six
import os
import re


class CallbackServer:
    ROOT = '/'
    ENDPOINT = '/awesome_endpoint/'
    URLS = {ROOT: index, ENDPOINT: endpoint}
    DEFAULT_HEADERS = {200: ('HTTP/1.1 200 OK\n\n', 200),   # \nContent-Type: text/css
                       404: ('HTTP/1.1 404 Not found\n\n', 404),
                       405: ('HTTP/1.1 405 Method not allowed\n\n', 405)}
    DEFAULT_CONTENT = {404: '<h1>404</h1><p>Not found<p>',
                       405: '<h1>405</h1><p>Method not allowed<p>'}
    DEBUG_SETTINGS = 'localhost', 8000
    ALG_CHOICE = {"Choice-Memoization": Execute.MEMOIZATION, "Choice-Tabulation": Execute.TABULATION}
    SELECTOR = selectors.DefaultSelector()
    LOGGER = logger
    CACHED_SETTINGS = None
    IDENT_PATTERN = re.compile(r'(?<=Choice-)(\S*)')

    def __init__(self, host=None, port=None, log_file="debug.json", level="DEBUG", rotation="100 KB"):
        serialize = True if ".json" in log_file else False
        CallbackServer.LOGGER.add(log_file, format="{time} {level} {message}", level=level,
                                  rotation=rotation, compression="zip", serialize=serialize)
        self._host = CallbackServer.DEBUG_SETTINGS[0] if host is None else host
        self._port = CallbackServer.DEBUG_SETTINGS[1] if port is None else port
        CallbackServer.CACHED_SETTINGS = self._host, self._port
        self._create_server()

    @staticmethod
    def parse_request(request):
        parsed = request.split(' ')
        method = parsed[0]
        url = parsed[1]
        return method, url

    def generate_headers(self, method, url):
        if url not in CallbackServer.URLS:
            return self.DEFAULT_HEADERS[404]
        if url == CallbackServer.ROOT and not method == 'GET':
            return self.DEFAULT_HEADERS[405]
        return self.DEFAULT_HEADERS[200]

    def generate_content(self, code, url, context):
        if code in (404, 405):
            return self.DEFAULT_CONTENT[code]
        return CallbackServer.URLS[url](context)

    def generate_response(self, request, payload):
        method, url = CallbackServer.parse_request(request)
        headers, code = self.generate_headers(method, url)
        payload = {'greeting': 'HELLO !!!'} if payload is None else payload
        payload['host'] = self._host
        payload['port'] = self._port
        body = self.generate_content(code, url, payload)
        return (headers + body).encode(), code

    @staticmethod
    def parse_body(body):
        if '&' in body:
            result = dict(tuple(item.split('=')) for item in body.split('&'))
            cleared_result = {k: v for k, v in result.items() if v}
            del cleared_result['Algo']
            stringy = any(alg in cleared_result.keys()
                          for alg in ('can_construct-arg1', 'count_construct-arg1', 'all_construct-arg1'))
            sequence = tuple(arg for arg in cleared_result.keys() if 'arg2' in arg and 'grid_traveller' not in arg)
            if sequence:
                arg2 = sequence[0]
                arg2_value = cleared_result[arg2].split('%2C')
                if all(elem.isdigit() for elem in arg2_value):
                    arg2_value = [int(value) for value in arg2_value]
                cleared_result[arg2] = arg2_value
            if not stringy:
                for k, v in cleared_result.items():
                    if 'Choice-' not in k and not isinstance(v, list):
                        try:
                            cleared_result[k] = int(v)
                        except ValueError:
                            cleared_result[k] = 1
            CallbackServer.LOGGER.debug(f"Parsed request body:\n{cleared_result}")
            return cleared_result

    def run_algo(self, raw_data):
        director = [self.ALG_CHOICE[key] for key in self.ALG_CHOICE.keys() if key in raw_data][0]
        args = []
        algorithm = None
        approach = (re.search(self.IDENT_PATTERN, key) for key in raw_data.keys() if re.search(self.IDENT_PATTERN, key))
        result = {'approach': next(approach).group()}
        for key, val in raw_data.items():
            if 'arg' in key:
                args.append(val)
                algorithm = key.split("-")[0]
        # if isinstance(data, Iterable) and not isinstance(data, six.string_types):
        #     return director.value.construct(op_num, *data)
        # else:
        #     return director.value.construct(op_num, data)
        if len(args) == 1:
            result.update(director.value.construct(algorithm, args[0]))
        else:
            result.update(director.value.construct(algorithm, *args))
        return result

    def _create_server(self):
        CallbackServer.LOGGER.debug(f"Attempt to create server on {self._host}:{self._port}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self._host, self._port))
        server_socket.listen()
        CallbackServer.SELECTOR.register(
            fileobj=server_socket, events=selectors.EVENT_READ, data=self.accept_connection)
        CallbackServer.LOGGER.info(f"{self._host}:{self._port} listening")

    def accept_connection(self, server_socket):
        client_socket, address = server_socket.accept()
        CallbackServer.SELECTOR.register(
            fileobj=client_socket, events=selectors.EVENT_READ, data=self.send_message)
        CallbackServer.LOGGER.debug(f"Accepted connection {client_socket} with {address}")

    def send_message(self, client_socket):
        request = client_socket.recv(4096)
        result = None
        # if request[-1] == '/':
        #     client_socket.send(b'Content-Type: text/html\n\n')
        #     client_socket.sendfile(open('.templates{os.sep}index.html', 'rb'))
        #     # client_socket.sendfile(open('.templates{os.sep}script.js', 'rb'))
        # else:
        #     if '.js' in request[-1]:
        #         client_socket.send(b'Content-Type: text/javascript\n\n')
        #     elif '.css' in request[-1]:
        #         client_socket.send(b'Content-Type: text/css\n\n')
        #     else:
        #         client_socket.send(b'None')
        #     client_socket.sendfile(open('.' + request[-1], 'rb'))
        if request:
            content = request.decode('utf-8')
            CallbackServer.LOGGER.info(f"Received request from {client_socket}")
            CallbackServer.LOGGER.debug(f"Request content:\n{content}")
            headers, body = content.split('\r\n\r\n')
            parsed_body = CallbackServer.parse_body(body)
            if parsed_body is not None:
                CallbackServer.LOGGER.debug(parsed_body)
                result = self.run_algo(parsed_body)
                CallbackServer.LOGGER.info(result)
            response, code = self.generate_response(request.decode('utf-8'), result)
            client_socket.send(response)
            CallbackServer.LOGGER.info(f"Generated response with status code: {code}")
        CallbackServer.SELECTOR.unregister(client_socket)
        client_socket.close()
        CallbackServer.LOGGER.warning("Socket closed")

    def run_event_loop(self):
        CallbackServer.LOGGER.debug(f"Event loop started for socket on {self._host}:{self._port}")
        while True:
            events = CallbackServer.SELECTOR.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == '__main__':
    CallbackServer().run_event_loop()
