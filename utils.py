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

    def run_query_df(self, query: str) -> pd.DataFrame:
        """
        Query data in an SQL database and returns it
        as a DataFrame

        Parameters
        -----------
        query: An SQL query to extract data from a database
        """

        # self.cur.execute(query)
        df = pd.read_sql_query(query, self.conn)

        return df

    def run_query_li(self, query: str) -> list:
        """
        Query data in an SQL database and returns it
        as a list

        Parameters
        -----------
        query: An SQL query to extract data from a database
        """

        return self.cur.execute(query)

    def close_all(self) -> None:
        """
        Close the connection to the database
        """
        self.cur.close()
        self.conn.close()
