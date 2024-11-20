import psycopg2
from read_and_preprocc_pdf import add_vectors_to_chunks, read_and_preprocc_some_text
from tqdm import tqdm
import os

def faiss_vectors():
    pass

path_to_pdfs = "/home/whoissleep/Документы/VS_CODE/proj/pdfs"

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

    def insert_data(self, dict_of_data):
        """
        Inserts the provided text and vectors into the TextVectors table.

        Args:
            text (list of str): The text data to be inserted as an array of strings.
            vectors (list of float): The vector data to be inserted as an array of floats.

        This method commits the transaction after the insertion.
        """
        text = dict_of_data['text']
        vectors = dict_of_data['vectors']
        vectors = [[vector.tolist() for vector in sublist] for sublist in vectors]

        cursor = self.conn.cursor()
        for t, v in zip(text, vectors):
            cursor.execute(
                "INSERT INTO TextVectors (text, vectors) VALUES (%s, %s)",
                ([t], v)
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
        
    def close_connection(self):
        """
        Closes the connection to the database.

        This method does not return anything, but prints a message to the console when the connection is closed.
        """
        self.conn.close()
        print("[INFO] CONNECTION CLOSED!!!")

    def add_to_db(self, num_of_docs):
        df = {"text": [], "vectors": []}

        for i in range(num_of_docs):
            pdf = read_and_preprocc_some_text(os.path.join(path_to_pdfs, f"{i + 1}.pdf"))
            pdf = add_vectors_to_chunks(pdf)
            for j in tqdm(range(len(pdf))):
                text_chunks = pdf[j]['sents_chunks']
                vector_chunks = pdf[j]['vectors']
                df['text'].append(text_chunks)
                df['vectors'].append(vector_chunks)

        self.insert_data(df)

    def count_values(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM TextVectors;"
        )
        row_count = cursor.fetchone()[0]
        cursor.close()
        return row_count

###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"