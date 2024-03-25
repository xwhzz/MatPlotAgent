"""
test.py

模拟客户端请求 100个req
"""

import aiohttp
import asyncio

async def fetch(session, url, data, delay):
    await asyncio.sleep(delay)
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    url = "http://127.0.0.1:8000/test"
    data = {
        "prompt": "",
        "csv": "",
    }

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, data, i + 1) for i in range(10)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


