import asyncio
import logging
import threading
from pprint import pformat

import socketio
from aiohttp import web
# import nest_asyncio
# nest_asyncio.apply()


class SocketServer:
    sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*", logger=True, engineio_logger=True)

    app = web.Application()
    sio.attach(app)

    @classmethod
    def aiohttp_server(cls):
        app = web.Application()
        cls.sio.attach(app)
        runner = web.AppRunner(app)
        return runner

    def run_server(self, host, port, runner):
        self.call_backs()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host, port)
        loop.run_until_complete(site.start())
        loop.run_forever()

    def run(self):
        self.call_backs()
        web.run_app(self.app,host="0.0.0.0", port=8001)

    def call_backs(self):
        @self.sio.event
        async def connect(sid, environ):
            logging.info(f"Socket from {str(sid)} is connected.")

        @self.sio.event
        async def disconnect(sid):
            logging.info(f"Socket from {str(sid)} is disconnected")

        @self.sio.on("add_camera")
        async def add(sid, data):
            if data:
                logging.info("\033[1;34m" + f'Received data: {pformat(data, indent=4)} from client.' + "\033[0;0m")

            return {"status": "OK"}

        @self.sio.on("edit")
        async def edit(sid, data):
            if data:
                logging.info(f'Edited data: {pformat(data, indent=4)}')

        @self.sio.on('remove')
        async def remove(sid, data):
            if data:
                logging.info(f"Removed data: {pformat(data, indent=4)}")

        @self.sio.on('send_message')
        async def send_message(sid, data):
            if data:
                logging.info('Server get the message: '+ str(data))
            await asyncio.sleep(1)
            await self.sio.emit('send_message', {"message":'Sever sending a message'})


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(filename)s|%(funcName)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)
    server = SocketServer()
    # server.run(server.aiohttp_server())
    # server.run()
    runner = server.aiohttp_server()
    threading.Thread(target=server.run_server, args=['0.0.0.0', 8001, runner]).start()
