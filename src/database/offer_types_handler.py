from typing import List, Tuple

from .table_handler import TableHandler


class OfferTypeItemsHandler(TableHandler):
    """
    Offer types table handling.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist.
        sql_query = self._get_sql_query("create_offer_types_table.sql")
        self._execute(sql_query, ())
    
    def _is_offer_type_item(self, offer_type_item: str) -> bool:
        """Returning True if there is offer_type_item in table."""
        sql_query = self._get_sql_query("is_offer_type_item.sql")
        result = self._execute(sql_query, (offer_type_item, ), fetchall=True)

        return len(result) > 0

    def add_offer_type_item(self, offer_type: str, offer_type_item: str, offer_type_city: str,
                            offer_type_item_url: str, strict_match_flag: bool) -> bool:
        """
        Adding offer into the table if it hasn't been added before.
        """
        if self._is_offer_type_item(offer_type_item):
            return False

        else:
            sql_query = self._get_sql_query("add_offer_type_item.sql")
            self._execute(sql_query,
                          (offer_type, offer_type_item, offer_type_city, offer_type_item_url, strict_match_flag)
            )
            return True

    def get_offer_type_item_id(self, offer_type_item: str) -> int:
        """
        Getting offer type_item_id by offer_typ_item.
        """
        if self._is_offer_type_item(offer_type_item):
            sql_query = self._get_sql_query("get_offer_type_item_id.sql")
            print(sql_query)
            offer_type_item_id = self._execute(sql_query, (offer_type_item, ), fetchall=True)[0][0]
            return offer_type_item_id

        else:
            return 0

    def get_all_offer_types(self) -> List[Tuple[str]]:
        """
        Getting all offer_types from table.
        Returns the list of tuples where every tuple have
        1. offer_type_item_id
        2. offer_type
        3. offer_type_item
        4. offer_type_item_url
        """
        sql_query = self._get_sql_query("get_all_offer_type_items_rows.sql")
        rows = self._execute(sql_query, (), fetchall=True)
        return rows

    def get_offer_type_title(self, offer_type_item_id: int) -> str:
        """Getting offer type title by offer type item id."""
        sql_query = self._get_sql_query("get_offer_type_title_by_offer_type_item_id.sql")
        print(sql_query, offer_type_item_id)

        offer_type = self._execute(sql_query, (offer_type_item_id, ), fetchall=True)[0]

        if offer_type:
            offer_type_title = offer_type[0]
            return offer_type_title

        else:
            return ""