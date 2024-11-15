import requests
import time
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass

from core import config
import database

@dataclass
class AvitoOffer:
    """Class for storing Avito offers."""
    type_id: int = -1
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
        self.users_handler = database.UsersHandler()
        self.offers_handler = database.OffersHandler()
        self.sellers_handler = database.SellersHanlder()
        self.user_offer_types_handler = database.UserOfferTypesHandler()
        self.offer_types_handler = database.OfferTypeItemsHandler()
        self.offer_queue_handler = database.OfferQueueHandler()

    def run(self) -> None:
        """
        Launching the infinite parser loop.
        """
        print("Parser settled up")
        while True:
            all_offer_types = self.offer_types_handler.get_all_offer_types()

            for offer_type in all_offer_types:
                offer_type_offers = self.parse_page(offer_type[4])
                strict_match_flag = offer_type[5]

                for offer in offer_type_offers:

                    # Checking for strict match
                    if strict_match_flag and not self._is_strict_match(offer.title, offer_type[2]):
                        continue

                    is_new = self.offers_handler.add_offer(
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
                    
                    if is_new:
                        offer_id = self.offers_handler.get_offer_id(offer.id)
                        self.offer_queue_handler.add_offer(offer_type[0], offer_id)
                        # print("ADDED")

                # In case there is not proxy.
                if config.PROXY_CHANGE_URL == "":
                    time.sleep(5)

    def parse_page(self, offer_type_item_page_url: str) -> List[AvitoOffer]:
        """Parsing all offers from the page."""
        base_url = "https://www.avito.ru"

        # page_request = base_url + f"/{city}?q={q}&p={p}"
        if config.PROXY["http"] != "":
            response = requests.get(offer_type_item_page_url, proxies=config.PROXY)
        else:
            response = requests.get(offer_type_item_page_url)

        if response.status_code != 200 and config.PROXY_CHANGE_URL != "":
            print("PARSER CHANGE")
            requests.get(config.PROXY_CHANGE_URL)
            return []

        page_html = response.text
        page_html_soup = BeautifulSoup(page_html, "lxml")
        main_offers_soup = page_html_soup.find("div", class_="items-items-pZX46")

        offers = []

        # Sometimes main_offers_soup is None.
        if not main_offers_soup:
            return []

        for div_offer in main_offers_soup.find_all("div", class_="iva-item-root-Se7z4"):
            
            offer = AvitoOffer()

            # There are problems with no description, no seller and e.g. problems.

            try:
                offer.id = div_offer.get("id")
            except:
                pass

            try:
                offer.title = div_offer.find("h3", class_="iva-item-title-CdRXl").text
            except:
                pass

            try:
                offer.description = div_offer.find("div", class_="iva-item-descriptionStep-i2icy").text
            except:
                pass

            try:
                # Splitting price and currency.
                span_price = div_offer.find("span", class_="iva-item-priceStep-TIzu3").text
                price_and_currency = span_price.split(u'\xa0')
                currency = price_and_currency[-1]
                price = "".join(price_and_currency[:-1])


                if price:
                    price = int(price)

                else:
                    price = 0

                offer.price = price
                offer.currency = currency
            except:
                pass

            # Idk why, but some offers haven't sellers.
            # seller_div = div_offer.find("div", class_="style-title-_wK5H")
            # if seller_div: offer.seller = seller_div.text

            # The same problem with seller ratings.
            # seller_rating_div = div_offer.find("span", class_="desktop-1lslbsi")
            # if seller_rating_div: offer.seller_rating = seller_rating_div.text

            try:
                offer.url = base_url + div_offer.find("a", class_="iva-item-sliderLink-Fvfau").get("href")

            except:
                pass

            offers.append(offer)
        
        return offers

    def _is_strict_match(self, offer_title: str, offer_type_item: str):
        """Checking that offer_type_item contains every word from offer_title."""
        offer_title_words = [word.lower() for word in offer_title.split()]
        offer_type_item_word = [word.lower() for word in offer_type_item.split()]

        return all(word in offer_type_item_word for word in offer_title_words)


def run_parser():
    avito_parser = AvitoParser()

    while True:
        try:
            avito_parser.run()
        except KeyboardInterrupt as e:
            break
        except:
            print("INTERNET CONNECTION")

if __name__ == "__main__":
    run_parser()
