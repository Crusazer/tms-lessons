import random
import asyncio
import time


async def generator():
    number = random.randint(1, 10)
    print(f"Await {number}s")
    await asyncio.sleep(number)
    print(f"Finish")


async def main():
    # tasks = [generator() for _ in range(100)]
    # await asyncio.gather(*tasks)
    tasks = [asyncio.create_task(generator()) for _ in range(100)]
    for task in tasks:
        await task


time_start = time.time()
asyncio.run(main())
time_end = time.time()
print(time_end - time_start)
