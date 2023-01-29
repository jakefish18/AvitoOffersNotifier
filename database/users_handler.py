from .table_handler import TableHandler


class UsersHanlder(TableHandler):
    """
    Users table handler.
    Contains functions to delete/add user.
    """

    def __init__(self) -> None:
        super().__init__()
        self.open_connection()

        # Creating table if it doesn't exist.
        sql_query = self._get_sql_query("create_users_table.sql")
        self._execute(sql_query, ())

    def _is_user(self, telegram_id: int) -> bool:
        """Returngs True if user with the same telegram_id exists."""
        sql_query = self._get_sql_query("is_user.sql")
        result = self._execute(sql_query, (telegram_id, ), fetchall=True)
        return len(result) != 0

    def add_user(self, telegram_id: int) -> bool:
        """
        Adding new user into the table.
        """
        if self._is_user(telegram_id):
            return False

        else:
            sql_query = self._get_sql_query("add_user.sql")
            self._execute(sql_query, (telegram_id, ))
            return True

    def del_user(self, user_id: int) -> None:
        """It's useless now :)"""
        pass


if __name__ == "__main__":
    users_handler = UsersHanlder("database/database_config.json")

    users_handler.add_user(12321341)
