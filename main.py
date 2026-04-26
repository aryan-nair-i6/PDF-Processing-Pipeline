import asyncio
from AsyncServices.discoverFile import discover
from AsyncServices.extractText import extract
from AsyncServices.summarizeText import summarize
from AsyncServices.loadVdb import load


discoverout = asyncio.Queue(maxsize=10)
extractout = asyncio.Queue(maxsize=7)
summarizeout = asyncio.Queue(maxsize=5)


async def main():
    tasks = [
        asyncio.create_task(discover(outqueue=discoverout)), 
        asyncio.create_task(extract(inqueue=discoverout, outqueue=extractout)),
        asyncio.create_task(summarize(inqueue=extractout, outqueue=summarizeout)),
        asyncio.create_task(load(inqueue=summarizeout)),
    ]

    await asyncio.gather(*tasks)


asyncio.run(main())