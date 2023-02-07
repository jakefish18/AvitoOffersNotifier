import psycopg2
import json

from typing import List, Tuple

PATH_TO_DATABASE_CONFIG = "/root/AvitoOffersNotifier/database/database_config.json"
with open(PATH_TO_DATABASE_CONFIG, "r") as file:
    database_config = json.load(file)


class TableHandler:
    """
    Base table handler class.
    """
    def __init__(self) -> None:
        self.database_host = database_config["DATABASE_HOST"]
        self.database_username = database_config["DATABASE_USERNAME"]
        self.database_name = database_config["DATABASE_NAME"]
        self.database_password = database_config["DATABASE_PASSWORD"]

        self.path_to_sql_queries = database_config["PATH_TO_SQL_QUERIES"]

    def open_connection(self) -> None:
        """
        Connecting to the database. 
        Every table handler instance creates a connection.
        """
        self.connection = psycopg2.connect(
            host=self.database_host,
            user=self.database_username,
            dbname=self.database_name,
            password=self.database_password
        )

    def close_connection(self) -> None:
        """Closing a database connection."""
        self.connection.close()

    def _create_cursor(self) -> None:
        """Creating a cursor to proccess query."""
        self.cursor = self.connection.cursor()

    def _close_cursor(self) -> None:
        """Closing a database connection cursor."""
        self.cursor.close()

    def _fetchone(self) -> Tuple:
        """Fetching one query return after the last fetch."""
        return self.cursor.fetchone()
    
    def _fetchall(self) -> List[Tuple]:
        """Fetching all query returns after the last fetch."""
        return self.cursor.fetchall()

    def _get_sql_query(self, sql_query_filename: str) -> str:
        """Retruning the sql query from file."""
        paht_to_sql_query = self.path_to_sql_queries + sql_query_filename
        sql_query = open(paht_to_sql_query, "r").read()
        return sql_query

    def _execute(self, query: str, data: tuple, fetchall: bool = False) -> List[Tuple]:
        """
        Execturing query with given data.
        Returning list of updated, deleted, selected, inserted rows if fetchall flag is setted to True
        else empty list with one empty tuple will be returned.
        """
        self._create_cursor()
        self.cursor.execute(query, data)
        self.connection.commit()

        if fetchall:
            query_results = self._fetchall()
            self._close_cursor()
            return query_results
        
        else:
            self._close_cursor()
            return [tuple()]
