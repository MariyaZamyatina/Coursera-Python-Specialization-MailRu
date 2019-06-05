import socket
import time


class ClientError(Exception):
    pass


class ClientSocketError(ClientError):
    pass


class ClientProtocolError(ClientError):
    pass


class Client:
    SERVER_END = '\n\n'
    SERVER_GOOD_MESSAGE = 'ok'
    SERVER_BAD_MESSAGE = 'error'

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self._sock = socket.create_connection((host, port), timeout=timeout)
        except (socket.error, socket.timeout):
            raise ClientSocketError('error create connection')

    def _write(self, data):
        try:
            self._sock.sendall(data.encode('utf8'))
        except (socket.error, socket.timeout):
            raise ClientSocketError("client error: write data")

    def _read(self):
        data = ''.encode('utf8')

        # get message from the server
        while not data.endswith(self.SERVER_END.encode('utf8')):
            try:
                data += self._sock.recv(1024)
            except socket.error as ex:
                raise ClientSocketError("client error: read data: " + ex)

        data = data.decode('utf8')

        # get correct message from server
        status, message = data.split('\n', 1)
        message = message.strip()

        if status == self.SERVER_GOOD_MESSAGE:
            return message
        elif status == self.SERVER_BAD_MESSAGE:
            raise ClientProtocolError(message)

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or str(int(time.time()))

        # send 'put' request to the server
        self._write('put {} {} {}\n'.format(key, value, timestamp))
        self._read()

    def get(self, key):
        # send 'get' request to the server
        self._write('get {}\n'.format(key))
        data = self._read()

        metrics_dict = {}

        if data == '':
            return metrics_dict

        metrics = data.split('\n')
        for metric in metrics:
            metric_key, metric_value, metric_timestamp = metric.split(' ')
            if metric_key not in metrics_dict:
                metrics_dict[metric_key] = []
            metrics_dict[metric_key].append((int(metric_timestamp), float(metric_value)))

        return metrics_dict

    def close(self):
        try:
            self._sock.close()
        except socket.error:
            raise ClientSocketError("error close connection")

