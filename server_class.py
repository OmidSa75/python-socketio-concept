import asyncio
import logging
import time
from threading import Thread

import socketio
from socketio.exceptions import ConnectionError
from aiohttp import web


class CObject:
    """
    Mutable object to track some changes in code
    """

    def __init__(self, value: bool):
        self.value = value

    def set(self, value):
        self.value = value

    def __repr__(self):
        return "_cobject value <" + str(self.value) + ">"

    def __bool__(self):
        return self.value


def wait_until_done(condition, delay_t, wait_time: int = 60):
    """
    Wait until the condition turns False before time out
    :param condition: desire condition to track
    :param delay_t: delay time
    :param wait_time: time out
    :return:
    """
    tic_time = time.time()
    while condition:
        time.sleep(delay_t)
        if time.time() - tic_time > wait_time:
            logging.warning("Wait Function Time out")
            return False
    logging.debug("Condition changed . . . !")
    return True


class ServerClass:
    def __init__(self):
        self.components = []
        self.not_finished = CObject(True)
        self.processing = False
        self.sio = socketio.AsyncServer(async_mode="aiohttp")
        self._server_loop = asyncio.new_event_loop()

    @property
    def server_loop(self):
        return self._server_loop

    def start_background_loop(self, loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_server(self):
        self.callbacks()
        app = web.Application()
        self.sio.attach(app)
        web.run_app(app, host='0.0.0.0', port=9000)

    async def run_server_2(self):
        app = web.Application()
        self.sio.attach(app)
        runner = web.AppRunner(app)
        self.callbacks()
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 9000)
        await site.start()
        await asyncio.Event().wait()

    def callbacks(self):

        @self.sio.event
        async def connect(sid, environ):
            logging.info('Socket connected')

        @self.sio.event
        async def disconnect(sid):
            logging.info('Socket disconnected')

        @self.sio.event
        async def connect_error(_):
            logging.error('Connection failed')

        @self.sio.event
        async def response(sid, log):
            logging.info(log)

        @self.sio.event
        async def execute(_):
            self.processing = True
            asyncio.run_coroutine_threadsafe(self.execute__(), self._server_loop)

        @self.sio.event
        async def add(_, data):
            if data:
                logging.info("Received data: {}".format(data))
                await self.add(data)

        @self.sio.event
        async def terminate(_):
            self.processing = False

    async def execute__(self):
        logging.info('Execution started . . .')
        self.processing = True
        self.not_finished.set(True)
        while self.processing:
            # await asyncio.sleep(5)
            time.sleep(1)
            logging.info('want to send result')
            await self.sio.emit('response', 'Results from server')
            logging.info('result sent')
        self.not_finished.set(False)
        logging.info("process stopped")

    async def add(self, data):
        logging.info('adding data')
        await self._add(data)
        logging.info("add another data")
        await self.sio.emit('add_another')

    async def _add(self, data):
        logging.info("want to add data")
        self.stop_processing()
        self.setup_data(data)
        self.start_processing()

    def stop_processing(self):
        logging.info('stop processing')
        if self.processing:
            self.processing = False
            wait_until_done(self.not_finished, 0.1, 10)

    def setup_data(self, data):
        logging.info('setup data . . .')
        self.components.append(data)
        time.sleep(2)

    def start_processing(self):
        asyncio.run_coroutine_threadsafe(self.execute__(), self._server_loop)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s-%(asctime)s::%(message)s', level=logging.DEBUG)
    server = ServerClass()
    Thread(target=server.start_background_loop, args=(server.server_loop,)).start()
    # server.run_server()
    asyncio.run_coroutine_threadsafe(server.run_server_2(), server.server_loop)
    logging.info('*'*80)
