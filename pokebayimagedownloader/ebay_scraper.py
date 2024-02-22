from typing import List
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict


@dataclass
class EbaySale:
    title: str
    image: str


class EbayScraper:
    """
    A simple eBay scraper for searching and extracting sale images and titles
    """
    base_url = "https://www.ebay.com/"

    def __init__(self):
        self.session = self._create_session()
        
    def _create_session(self) -> httpx.Client:
        headers = {"Accept-Language": "en-US;q=0.8,en;q=0.7"}
        s = httpx.Client(headers=headers)
        return s

    def search(self, query: str) -> HTMLParser:
        """
        Perform a search on eBay and return the HTML content of the search results page

        :param query: The search query
        :return: The HTML content of the eBay search results page
        """
        search_url = self.base_url + f"sch/i.html?_from=R40&_nkw={query.replace(' ', '+')}&_sacat=0&_sop=15"
        print(search_url)
        resp = self.session.get(search_url)
        return HTMLParser(resp.text)

    def get_sales_info(self, html_parser: HTMLParser) -> List[dict]:
        """
        Extract sale infos from the eBay search results HTML.

        :param html_parser: The HTML content of the eBay search results page.
        :return: A list of sale dict.
        """
        card_sales = html_parser.css("div.s-item__wrapper")
        results = []

        for sale in card_sales:
            new_card_sale = EbaySale(
                title=sale.css_first("span[role='heading']").text(),
                image=sale.css_first("img").attributes["src"]
            )
            results.append(asdict(new_card_sale))

        return results[1:]
