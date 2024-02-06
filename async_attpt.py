import asyncio

async def make_caption(file_name):
    await asyncio.sleep(1)
    print(f"Made caption {file_name}")

async def make_images(file_name):
    await asyncio.sleep(5)
    print(f"Made images {file_name}")

async def make_video(file_name):
    await asyncio.sleep(10)
    print(f"Made video {file_name}")

async def main():
    tasks = []

    for counter in range(1, 11):
        file_name = str(counter)
        caption_task = asyncio.create_task(make_caption(file_name))
        image_task = asyncio.create_task(make_images(file_name))
        await caption_task
        await image_task
        video_task = asyncio.create_task(make_video(file_name))
        tasks.append(video_task)

    await asyncio.gather(*tasks)

asyncio.run(main())
