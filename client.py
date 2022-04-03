import asyncio
import atexit
import json
import logging
import threading
from pprint import pformat
import time

import socketio
from aiohttp import web
# import nest_asyncio
# nest_asyncio.apply()


class SocketClient:
    client_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_loop)
    sio = socketio.AsyncClient(logger=True)

    async def add_camera(self, cam: dict):
        await self.sio.emit('add_camera', cam, callback=self.callback_fn())
        # task = asyncio.create_task(self.sio.emit('add_camera', cam))
        logging.info("Sent Message")
        return

    @staticmethod
    def callback_fn():
        logging.info("\033[1;34m" + "this is the callback function "+"\033[0;0m")

    async def edit_camera(self, cam: dict):
        await self.sio.emit('edit_camera', cam)

    async def remove_camera(self, cam: dict):
        await self.sio.emit('remove_camera', cam)

    async def sending_cameras(self):
        while True:
            time.sleep(5)
            await self.add_camera({'cam':'OmidSa75'})

    def call_backs(self):
        @self.sio.event
        async def connect():
            logging.info(f"Socket connected")
            # await self.sio.emit('send_message', {'message':"I am client"})

        @self.sio.event
        async def response(data):
            print('message received with ', data)

        @self.sio.event
        async def disconnect():
            logging.info(f"Socket disconnected")

        @self.sio.on('execute')
        async def execute():
            logging.info("Executing the process . . .")
            await self.execute()

        @self.sio.on('show_logs')
        async def show_logs(logs):
            logging.info(pformat(logs))

        @self.sio.on('send_message')
        async def send_message(data):
            if data:
                logging.info('Client received a message: '+ str(data))
            await asyncio.sleep(1)
            await self.sio.emit('send_message', {'message': "I am client"})

    async def execute(self):
        await self.sio.emit('execute')

    async def terminate(self):
        await self.sio.emit('terminate')

    async def run(self):
        # self.call_backs()
        await self.sio.connect("http://localhost:8001")
        await self.sio.wait()

    def run_from_thread(self):
        self.client_loop.run_until_complete(self.run())


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(filename)s|%(funcName)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)
    with open('cameras.json', 'r') as f:
        cam_samples = json.load(f)

    import threading
    client = SocketClient()
    client.call_backs()
    threading.Thread(target=client.run_from_thread).start()
    # threading.Thread(target=asyncio.run, args=[(client.run())]).start()
    # asyncio.run(client.run())

