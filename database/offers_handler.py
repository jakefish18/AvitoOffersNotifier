from database.table_handler import TableHandler
from avito_parser.avito_parser import AvitoOffer


class OffersHandler(TableHandler):
    """
    Offers table handling.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist.
        sql_query = self._get_sql_query("create_offers_table.sql")
        self._execute(sql_query, ())
    
    def _is_offer(self, offer_avito_id: int) -> bool:
        """Returning is offer with offer_avito_id in the offers table."""
        sql_query = self._get_sql_query("is_offer.sql")
        result = self._execute(sql_query, (offer_avito_id, ), fetchall=True)

        return len(result) > 0

    def add_offer(self, offer_type_id: int, offer_avito_id: int, offer_title: str,
            offer_city: str, offer_description: str, offer_price: int, offer_currency: str,
            seller_id: int, offer_url: str) -> bool:
                """
                Adding new offer into the table.
                """

                print(offer_city)

                if self._is_offer(offer_avito_id):
                    return False

                else:
                    sql_query = self._get_sql_query("add_offer.sql")
                    self._execute(
                        sql_query,
                        (offer_type_id, offer_avito_id, offer_title, offer_city,
                        offer_description, offer_price, offer_currency, seller_id, offer_url)
                    )
                    return True

    def get_offer_id(self, offer_avito_id: str):
        """
        Getting offer id by offer avito id.
        """
        sql_query = self._get_sql_query("get_offer_id_by_offer_avito_id.sql")
        offer = self._execute(sql_query, (offer_avito_id, ), fetchall=True)

        return offer[0][0]

    def get_offer_info(self, offer_id: int) -> AvitoOffer:
        """
        Getting offer info by offer_id.
        """
        offer = AvitoOffer()
        sql_query = self._get_sql_query("get_offer_info_by_offer_id.sql")
        offer_items = self._execute(sql_query, (offer_id, ), fetchall=True)[0]

        offer.type_id = offer_items[1]
        offer.id = offer_items[2]
        offer.title = offer_items[3]
        offer.city = offer_items[4]
        offer.description = offer_items[5]
        offer.price = offer_items[6]
        offer.currency = offer_items[7]
        offer.seller_id = offer_items[8]
        offer.url = offer_items[9]

        return offer