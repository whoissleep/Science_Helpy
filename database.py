import faiss
import psycopg2
import numpy as np

class PostgreDB:
    def __init__(self, dbname: str, user: str, password: str):
        """
    Initializes a connection to a PostgreSQL database.

    Args:
        dbname (str): The name of the database.
        user (str): The username used to authenticate.
        password (str): The password used to authenticate.

    Attributes:
        conn (psycopg2.connection): The connection object to the PostgreSQL database.
        """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port="5432"
        )
        print("[INFO] CONNECTED TO DB!!!")

    def create_database(self):
        """
        Creates the TextVectors table in the database if it does not exist.

        The TextVectors table has three columns: id, text, and vectors.
        The id column is the primary key and is an auto-incrementing integer.
        The text column stores the text data as an array of strings.
        The vectors column stores the precomputed vectors for the text data as an array of floats.

        This method does not return anything, but prints a message to the console when the table is created.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS TextVectors (
                id SERIAL PRIMARY KEY,
                text TEXT[] NOT NULL,
                vectors FLOAT8[] NOT NULL
            )
            """
        )
        self.conn.commit()
        print("[INFO] DB IS CREATED!!!")

    def insert_data(self, text, vectors):
        """
        Inserts the provided text and vectors into the TextVectors table.

        Args:
            text (list of str): The text data to be inserted as an array of strings.
            vectors (list of float): The vector data to be inserted as an array of floats.

        This method commits the transaction after the insertion.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO TextVectors (text, vectors)
            VALUES (%s, %s)
            """,
            (text, vectors)
        )
        self.conn.commit()
        cursor.close()

    def fetch_data(self):
        """
        Fetches all the data from the TextVectors table.

        Returns:
            rows (list of tuple): A list of tuples, where each tuple contains the text and vectors of a row in the table.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT text, vectors
            FROM TextVectors
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    

###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"