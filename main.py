import asyncio
import threading
import concurrent.futures
from pokebayimagedownloader.cards_image_downloader import CardsImageDownloader


def download_images_async(cards_downloader, set_id):
    asyncio.run(cards_downloader.download_by_set(set_id))


async def main():
    aux = CardsImageDownloader(img_qty=50)
    set_ids = ['sv3']
    tasks = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        loop = asyncio.get_event_loop()
        for set_id in set_ids:
            tasks.append(loop.run_in_executor(executor, download_images_async, aux, set_id))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
