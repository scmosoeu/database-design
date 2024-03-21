import pyodbc
import pandas as pd


class SQLConnector:
    """
    Create a connection to a database

    Parameters
    -----------
    config: login details to the database
    """

    def __init__(self, config: dict) -> None:
        self.conn = pyodbc.connect(**config)
        self.cur = self.conn.cursor()

    def run_query(self, query: str) -> list:
        """
        Query data in an SQL database and returns it
        as a list

        Parameters
        -----------
        query: An SQL query to extract data from a database
        """

        query_results = self.cur.execute(query)

        return query_results.fetchall()

    def close_all(self) -> None:
        """
        Close the connection to the database
        """
        self.cur.close()
        self.conn.close()
