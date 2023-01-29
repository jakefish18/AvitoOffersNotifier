import requests
import asyncio
import sys
import json
from bs4 import BeautifulSoup
from typing import List, Tuple
from dataclasses import dataclass

PATH_TO_PARSER_CONFIG = "/home/jakefish/Documents/GitHub/my/AvitoOffersNotifier/avito_parser/parser_config.json"
with open(PATH_TO_PARSER_CONFIG, "r") as file:
    parser_config = json.load(file)

sys.path.insert(0, parser_config["PATH_TO_PROJECT"])
import database


@dataclass
class AvitoOffer:
    """Class for storing Avito offers."""
    id: int = -1
    title: str = ""
    description: str = ""
    city: str = ""
    price: int = -1
    currency: str = "₽"
    seller: str = ""
    seller_rating: float = 0.0
    url: str = ""


class AvitoParser:
    """
    Yeah.
    """
    
    def __init__(self) -> None:
        self.users_handler = database.UsersHanlder()
        self.offers_handler = database.OffersHandler()
        self.sellers_handler = database.SellersHanlder()
        self.user_offer_types_handler = database.UserOfferTypes()
        self.offer_types_handler = database.OfferTypeItemsHandler()

    def run(self) -> None:
        all_offer_types = self.offer_types_handler.get_all_offer_types()

        for offer_type in all_offer_types:
            offer_type_offers = self.parse_page(offer_type[4])

            for offer in offer_type_offers:
                self.offers_handler.add_offer(
                    offer_type_id=int(offer_type[0]),
                    offer_avito_id=offer.id,
                    offer_title=offer.title,
                    offer_city=offer_type[3],
                    offer_description=offer.description,
                    offer_price=offer.price,
                    offer_currency=offer.currency,
                    seller_id=-1,
                    offer_url=offer.url
                )

    def parse_page(self, offer_type_item_page_url: str) -> List[AvitoOffer]:
        """Parsing all offers from the page."""
        base_url = "https://www.avito.ru"

        # page_request = base_url + f"/{city}?q={q}&p={p}"
        response = requests.get(offer_type_item_page_url)

        page_html = response.text
        page_html_soup = BeautifulSoup(page_html, "lxml")
        main_offers_soup = page_html_soup.find("div", class_="items-items-kAJAg")

        offers = []

        for div_offer in main_offers_soup.find_all("div", class_="iva-item-root-_lk9K"):
            
            offer = AvitoOffer()

            offer.id = div_offer.get("id")
            offer.title = div_offer.find("h3", class_="title-root-zZCwT").text
            offer.description = div_offer.find("div", class_="iva-item-text-Ge6dR").text
            
            # Splitting price and currency.
            span_price = div_offer.find("span", class_="price-text-_YGDY").text
            price_and_currency = span_price.split(u'\xa0')
            currency = price_and_currency[-1]
            price = "".join(price_and_currency[:-1])
            print(price, currency)

            if price:
                price = int(price)
            
            else: 
                price = 0

            offer.price = price
            offer.currency = currency

            # Idk why, but some offers haven't sellers.
            # seller_div = div_offer.find("div", class_="style-title-_wK5H")
            # if seller_div: offer.seller = seller_div.text
            
            # The same problem with seller ratings.
            # seller_rating_div = div_offer.find("span", class_="desktop-1lslbsi")
            # if seller_rating_div: offer.seller_rating = seller_rating_div.text

            offer.url = base_url + div_offer.find("a", class_="iva-item-sliderLink-uLz1v").get("href")

            offers.append(offer)
        
        return offers


if __name__ == "__main__":
    avito_parser = AvitoParser()
    avito_parser.run()
