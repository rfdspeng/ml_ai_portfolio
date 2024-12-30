import asyncio

async def c1():
    print("c1 before await")
    await c2()
    print("c1 after await")
    return

async def c2():
    x = 1
    print("c2: x = 1")
    await asyncio.sleep(1)
    print("c2: return")
    return x

async def main():
    await asyncio.gather(c1(), c1(), c1())

asyncio.run(main())