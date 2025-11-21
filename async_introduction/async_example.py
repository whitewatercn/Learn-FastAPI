import asyncio
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()


async def fetch_data(delay,id):
	print(f'start fetching {id}')
	await asyncio.sleep(delay)
	print(f'done fetching {id}')
	return {'data': f'some data {id}'}

async def main():
	task1 = fetch_data(2,1)
	task2 = fetch_data(2,2)
 
	result1 = await task1
	print(f'Received result1: {result1}')
	result2 = await task2
	print(f'Received result2: {result2}')

asyncio.run(main())


profiler.stop()

profiler.print()