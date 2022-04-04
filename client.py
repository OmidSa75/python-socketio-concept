# import asyncio
# import concurrent.futures
# import logging
# import threading
#
# import socketio
#
# logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s :: %(message)s')
# sio = socketio.AsyncClient(logger=True)
#
#
# @sio.event
# async def connect():
#     logging.info("Connected to server")
#
#
# @sio.event
# async def disconnect():
#     logging.info("Disconnected from server")
#
#
# async def run():
#     await sio.connect("http://0.0.0.0:9000")
#     await sio.wait()
#
#
# def run_(loop):
#     asyncio.run_coroutine_threadsafe(run(), loop)
#
#
# async def run_thread_safe():
#     loop = asyncio.get_event_loop()
#     executor = concurrent.futures.ThreadPoolExecutor()
#     await loop.run_in_executor(executor, run_, loop)
#
#
# # asyncio.run(run_thread_safe())
# # threading.Thread(target=asyncio.run, args=([run()])).start()
# loop = asyncio.new_event_loop()
# # executor = concurrent.futures.ThreadPoolExecutor()
# # asyncio.run(loop.run_in_executor(executor, run_, loop))
# future = asyncio.run_coroutine_threadsafe(run(), loop)
# # assert future.result(3.0) == 3
#
# # coro = asyncio.sleep(1, result=3)
# # future = loop.call_soon_threadsafe(coro)
# # assert future.result(3) == 3.0

'''New main'''
import asyncio
import concurrent.futures
import logging
import threading

import socketio

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s :: %(message)s')
sio = socketio.AsyncClient(logger=True)


@sio.event
async def connect():
    logging.info("Connected to server")


@sio.event
async def disconnect():
    logging.info("Disconnected from server")


async def run():
    await sio.connect("http://0.0.0.0:9000")
    await sio.wait()


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()

    task = asyncio.run_coroutine_threadsafe(run(), loop)