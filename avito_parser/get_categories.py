import requests
import time
import json

from typing import Dict
from bs4 import BeautifulSoup


# The parser uses Firefox avito.ru version for parsing.
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"}


def get_main_categories_urls() -> Dict[str, str]:
    """
    Parsing all main categories which placed on the https://avito.ru.
    Returning dict with [category_title: category_URL] structure.
    """
    avito_main_page_url = "https://avito.ru"
    avito_main_page_response = requests.get(avito_main_page_url, headers=headers)
    avito_main_page_html = avito_main_page_response.text
    avito_main_page_soup = BeautifulSoup(avito_main_page_html, "lxml")

    main_categories_urls = {}

    for main_category_div in avito_main_page_soup.find_all("div", class_="category-with-counters-item-HDr9u"):
        main_category_a = main_category_div.find("a", class_="link-link-MbQDP")
        main_category_title = main_category_a.text

        # Cleaning a city in the beginnning of the URL.
        # Splitted link have empty string and city in the beginning.
        main_category_url = "/".join(main_category_a.get("href").split("/")[2:])
        print(main_category_url)

        main_categories_urls[main_category_title] = main_category_url


    return main_categories_urls

def get_subcategories_urls(category_page_url: str) -> Dict[str, str]:
    """
    Parsing all subcategories of category.
    Returning dict with [subcategory_title: subcategory_URL] structure.
    """ 

    # TODO: Nedvizimost category has special page.
    if "nedvizhimost" in category_page_url:
        return {}

    category_page_response = requests.get(category_page_url, headers=headers)
    category_page_html = category_page_response.text
    category_page_soup = BeautifulSoup(category_page_html, "lxml")

    all_categories_list = category_page_soup.find("ul", class_="rubricator-list-item-submenu-bQ0A4")
    
    subcategories_urls = {}

    for subcategory in all_categories_list.find_all("li", class_="rubricator-list-item-item-WKnEv"):
        subcategory_a = subcategory.find("a", class_="rubricator-list-item-link-uPiO2")
        subcategory_title = subcategory_a.get("title")

        # Cleaning a city in the begining of the URL.
        subcategory_url = "/".join(subcategory_a.get("href").split("/")[1:])
        
        subcategories_urls[subcategory_title] = subcategory_url

    return subcategories_urls

def get_categories_urls() -> Dict[str, Dict[str, str]]:
    """
    Parsing all categories and their links.
    Returning dict with [main_category_title: subcategories_urls] structure,
    where subcategories_urls with [subctegory_title: subcategory_url] structure.
    """

    categories_urls = get_main_categories_urls()

    for main_category_title, main_category_url in categories_urls.items():
        subecategories_page_url = "https://avito.ru/all/" + main_category_url
        categories_urls[main_category_title] = get_subcategories_urls(subecategories_page_url)

        time.sleep(1)

    return categories_urls


if __name__ == "__main__":
    categories_urls = get_categories_urls()

    with open("./categories_urls.json", "w", encoding="utf8") as file:
        json.dump(categories_urls, file, ensure_ascii=False)