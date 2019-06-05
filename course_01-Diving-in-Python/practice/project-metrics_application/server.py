import asyncio


class Data:

    def __init__(self):
        self._metrics = {}

    def put(self, key, value, timestamp):
        if key not in self._metrics:
            self._metrics[key] = {}

        self._metrics[key][timestamp] = value

    def get(self, key):
        if key == '*':
            return self._metrics
        elif key in self._metrics:
            return {key: self._metrics[key]}
        else:
            return {}


class ClientServerProtocol(asyncio.Protocol):
    _server_commands = ['put', 'get']

    SERVER_OK_RESPONSE = 'ok\n\n'
    SERVER_ERROR_RESPONSE = 'error\nwrong command\n\n'

    _data = Data()

    def __init__(self):
        super().__init__()
        self._buffer = b''

    def _process_get(self, message):
        metric_key = message.split(' ')

        if len(metric_key) != 1:
            return self.SERVER_ERROR_RESPONSE

        metrics = self._data.get(metric_key[0])

        # { "k1": {1: 0.25, 2: 2.156, 3: 0.35}, "k2": {4: 30.0, 5: 40.0} }
        metrics_str = ''
        for key in metrics:
            for timestamp in metrics[key]:
                metrics_str += '{} {} {}\n'.format(key, metrics[key][timestamp], timestamp)

        if len(metrics) == 0:
            return self.SERVER_OK_RESPONSE
        else:
            return self.SERVER_OK_RESPONSE + metrics_str + '\n'

    def _process_put(self, message):
        metric = message.split(' ')

        if len(metric) != 3:
            return self.SERVER_ERROR_RESPONSE

        try:
            metric_key = metric[0]
            metric_value = float(metric[1])
            metric_timestamp = int(metric[2])
        except ValueError:
            return self.SERVER_ERROR_RESPONSE

        self._data.put(metric_key, metric_value, metric_timestamp)
        return self.SERVER_OK_RESPONSE

    def process_data(self, data):
        command, message = data.split(' ', 1)

        if command not in self._server_commands:
            return self.SERVER_ERROR_RESPONSE

        message = message.strip()
        if command == 'put':
            return self._process_put(message)
        if command == 'get':
            return self._process_get(message)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self._buffer += data
        decoded_data = self._buffer.decode()

        if not decoded_data.endswith('\n'):
            return

        self._buffer = b''

        resp = self.process_data(decoded_data)
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server('127.0.0.1', 8888)



