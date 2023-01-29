from .table_handler import TableHandler


class SellersHanlder(TableHandler):
    """
    Sellers table handling.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist.
        sql_query = self._get_sql_query("create_sellers_table.sql")
        self._execute(sql_query, ())
    
    def _is_seller(self, seller_avito_id: int):
        """Returning is seller with seller_avito_id in table."""
        sql_query = self._get_sql_query("is_seller.sql")
        result = self._execute(sql_query, (seller_avito_id, ))

        return len(result) > 0

    def add_seller(self, seller_avito_id: int, seller_name: str, seller_rating: float) -> bool:
        """
        Adding new seller into the table.
        """
        if self._is_seller(seller_avito_id):
            return False

        else:
            sql_query = self._get_sql_query("add_seller")
            self._execute(
                sql_query,
                (seller_avito_id, seller_name, seller_rating)
            )
            return True    