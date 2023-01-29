from .table_handler import TableHandler


class UserOfferTypes(TableHandler):
    """
    User offers table handling.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist
        sql_query = self._get_sql_query("create_user_offer_types_table.sql")
        self._execute(sql_query, ())

    def _is_user_offer_type_item(self, user_id: int, offer_type_item_id: int) -> bool:
        sql_query = self._get_sql_query("is_user_offer_type_item.sql")
        result = self._execute(sql_query, (user_id, offer_type_item_id))

        return len(result) > 0

    def add_user_offer_type_item(self, user_id: int, offer_type_item_id: int) -> bool:
        """Adding new user offer type item."""
        if self._is_user_offer_type_item(user_id, offer_type_item_id):
            return False

        else:
            sql_query = self._get_sql_query("add_user_offer_type_item.sql")
            self._execute(sql_query, (user_id, offer_type_item_id))
            return True
    