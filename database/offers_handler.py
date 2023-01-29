from .table_handler import TableHandler


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