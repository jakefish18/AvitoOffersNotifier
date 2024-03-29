from database.table_handler import TableHandler

from typing import List, Tuple

class OfferQueueHandler(TableHandler):
    """
    Offers queue table handler.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist.
        sql_query = self._get_sql_query("create_offer_queue_table.sql")
        self._execute(sql_query, ())

    def _is_offer(self, offer_id: int) -> bool:
        """
        Returning is offer in queue.
        """
        sql_query = self._get_sql_query("is_offer_in_queue.sql")
        result = self._execute(sql_query, (offer_id, ), fetchall=True)

        return len(result) > 0

    def add_offer(self, offer_type_id: int, offer_id: int):
        """
        Adding new offer into the notification queue.
        Returning True if offer didn't exist.
        """
        if self._is_offer(offer_id):
            return False

        else:
            sql_query = self._get_sql_query("add_offer_to_queue.sql")
            self._execute(sql_query, (offer_type_id, offer_id))
            return True

    def get_offers(self) -> List[Tuple[str]]:
        """
        Getting all offers from queue with delete.
        """
        sql_query = self._get_sql_query("get_offer_queue.sql")
        offers = self._execute(sql_query, (), fetchall=True)

        return offers
