import asyncio
import time
import sys

if len(sys.argv) > 1:
    async_flag = sys.argv[1]
else:
    async_flag = False

if async_flag: # asynchronous code
    async def count(): # coroutine
        print("One")
        await asyncio.sleep(1)
        print("Two")
        await asyncio.sleep(1)

    async def main(): # coroutine
        await asyncio.gather(count(), count(), count()) # use gather() to run coroutines concurrently

else: # synchronous code
    def count():
        print("One")
        time.sleep(1)
        print("Two")
        time.sleep(1)

    def main():
        count()
        count()
        count()

s = time.perf_counter()
if async_flag:
    asyncio.run(main()) # run() starts an event loop to run the passed coroutine and shuts down the event loop after coroutine finishes
else:
    main()
elapsed = time.perf_counter() - s
print(f"Program executed in {elapsed:0.2f} seconds.")