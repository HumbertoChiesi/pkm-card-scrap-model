import asyncio
import os
import pathlib
from typing import List
from dataclasses import dataclass

import aiohttp

import urllib.parse
from pokemontcgsdk import Set
from pokebayimagedownloader.cards_info import CardsInfo
from pokebayimagedownloader.ebay_scraper import EbayScraper


@dataclass
class PokeSet:
    set_printed_total: str
    set_year_released: str


class CardsImageDownloader:
    """
       A class for downloading Pokemon trading card images from eBay.

       Attributes:
           base_directory (str): Directory where the downloaded images will be saved.
           ebay_scraper (EbayScraper): Instance of the EbayScraper class used for scraping eBay.
           MAX_RELATED_SALES (int): The maximum number of related sales to download.
    """

    def __init__(self, saving_directory: str = './files/images', img_qty: int = 10):
        self.base_directory = saving_directory
        self.ebay_scraper = EbayScraper()
        self.MAX_RELATED_SALES = img_qty

    def _build_query(self, card_name: str, card_id: str, poke_set: PokeSet) -> str:
        card_number = card_id.split('-')[1]
        query = f"pokemon {urllib.parse.quote(card_name)} {card_number}/{poke_set.set_printed_total} {poke_set.set_year_released}"
        return query

    def _get_set_info(self, set_id: str) -> PokeSet:
        try:
            set_info = Set.find(set_id)
        except Exception:
            raise ValueError(f"Could not find set: {set_id}")

        poke_set = PokeSet(
            set_printed_total=set_info.printedTotal,
            set_year_released=set_info.releaseDate[0:4]
        )

        return poke_set

    def _get_ebay_info(self, query: str) -> List[dict]:
        sales_info = self.ebay_scraper.get_sales_info(
            self.ebay_scraper.search(query)
        )

        return sales_info

    def _get_sales_images(self, card_name: str, card_id: str, poke_set: PokeSet) -> List[str]:
        ebay_sales = self._get_ebay_info(self._build_query(card_name, card_id, poke_set))
        images_url = [sale['image'] for sale in self._remove_unrelated_sales(ebay_sales, card_name, card_id, poke_set)]

        return images_url

    def _remove_unrelated_sales(self, sales_list: List[dict], card_name: str, card_id: str, poke_set: PokeSet) -> List[
        dict]:
        card_number = card_id.split('-')[1]
        related_sales = []

        for card_sale in sales_list:
            if card_name.lower() in card_sale['title'].lower() and f"{card_number}/{poke_set.set_printed_total}" in \
                    card_sale['title'].lower():
                related_sales.append(card_sale)

        return related_sales[
               :(self.MAX_RELATED_SALES if (len(related_sales) > self.MAX_RELATED_SALES >= 0) else len(related_sales))]

    async def _download_image(self, session: aiohttp.ClientSession, image_url: str, file_path: str) -> None:
        async with session.get(image_url) as response:
            if response.status != 200:
                return None
            with open(file_path, 'wb') as file:
                file.write(await response.read())

    async def _iterate_images(self, images_url: List[str], card_id: str, image_path: pathlib.Path) -> None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for index, image_url in enumerate(images_url):
                file_path = os.path.join(image_path, f"{card_id}_{index + 1}.jpg")
                tasks.append(self._download_image(session, image_url, file_path))
            await asyncio.gather(*tasks)

    async def download_card_images(self, card_name: str, card_id: str, poke_set: PokeSet) -> None:
        images_url = self._get_sales_images(card_name, card_id, poke_set)

        image_path = self.base_directory + f"/{card_id}"
        os.makedirs(image_path, exist_ok=True)

        await self._iterate_images(images_url, card_id, pathlib.Path(image_path))

    async def download_by_set(self, set_id: str) -> None:
        poke_set = self._get_set_info(set_id)
        print(poke_set)
        set_cards_df = CardsInfo.get_by_sets([set_id], ['name', 'id'])

        for index, row in set_cards_df.iterrows():
            await self.download_card_images(row['name'], row['id'], poke_set)
