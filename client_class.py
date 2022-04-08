import asyncio
import logging
from collections import deque
from threading import Thread

import socketio
from socketio.exceptions import ConnectionError


class ClientClass:
    def __init__(self):
        self.connected = False
        self.sio = socketio.AsyncClient(handle_sigint=True)
        self._client_loop = asyncio.new_event_loop()
        self._adding_flag = False
        self._add_queue = deque()

    def start_background_loop(self, loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @property
    def client_loop(self):
        return self._client_loop

    async def run(self):
        self.callbacks()
        try:
            await self.sio.connect('http://{}:{}'.format('0.0.0.0', 9000))
        except ConnectionError:
            logging.error('connection failed.')

        await self.sio.wait()

    def callbacks(self):
        @self.sio.event
        async def connect():
            self.connected = True
            logging.info('Socket connected')

        @self.sio.event
        async def disconnect():
            self.connected = False
            logging.info('Socket disconnected')

        @self.sio.event
        async def connect_error(_):
            self.connected = False
            logging.error('Connection failed')

        @self.sio.event
        async def response(log):
            logging.info(log)
            
        @self.sio.event
        async def add_another():
            await self._add()

    async def send_message(self, message):
        await self.sio.emit('response', 'This is the message from client')

    async def _add(self):
        logging.info('_add function')
        if not self.connected:
            return 
        
        if len(self._add_queue) > 0:
            logging.info('emit add')
            await self.sio.emit('add', self._add_queue.pop())
        else:
            logging.info('set adding flag to false')
            self._adding_flag = False

    async def add(self, data):
        logging.info('Adding data to queue')
        self._add_queue.append(data)
        if not self._adding_flag:
            await self._add()
            self._adding_flag = True


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s-%(asctime)s::%(message)s', level=logging.DEBUG)
    client = ClientClass()
    Thread(target=client.start_background_loop, args=(client.client_loop, ), daemon=True).start()
    asyncio.run_coroutine_threadsafe(client.run(), client.client_loop)

