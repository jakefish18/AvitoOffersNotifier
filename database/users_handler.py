from database.table_handler import TableHandler


class UsersHandler(TableHandler):
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
        """Returning True if user with the same telegram_id exists."""
        sql_query = self._get_sql_query("is_user.sql")
        result = self._execute(sql_query, (telegram_id, ), fetchall=True)
        return len(result) > 0

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

    def get_user_id(self, telegram_id: int) -> int:
        """
        Getting user id by telegram id.
        """
        if self._is_user(telegram_id):
            sql_query = self._get_sql_query("get_user_id.sql")
            user_id = self._execute(sql_query, (telegram_id, ), fetchall=True)[0][0]
            return user_id

        else:
            return 0

    def get_user_telegram_id(self, user_id: int) -> int:
        """
        Getting user telegram id by user id.
        """
        sql_query = self._get_sql_query("get_user_telegram_id.sql")
        user_telegram_id = self._execute(sql_query, (user_id, ), fetchall=True)[0][1]
        return user_telegram_id


if __name__ == "__main__":
    users_handler = UsersHandler("database/database_config.json")

    users_handler.add_user(12321341)
