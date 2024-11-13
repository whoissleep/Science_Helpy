from download_pdf import download_all_papers
from read_and_preprocc_pdf import read_and_preprocc_some_text, add_vectors_to_chunks
from database import PostgreDB
from vectorizer import Vectorizer
from model_api import ChatModel
from dotenv import load_dotenv
import os
from tqdm.auto import tqdm
import pandas as pd

def main():
    path_to_pdfs = "/home/whoissleep/Документы/VS_CODE/proj/pdfs"
    num_of_docs = len(os.listdir(path_to_pdfs))
    api_key = os.getenv("HF_API")
    model_id = "Qwen/Qwen2.5-72B-Instruct"
    vectorizer = Vectorizer()
    chat_model = ChatModel(api_key=api_key, model_id=model_id)
    database = PostgreDB(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
    download_all_papers()
    database.create_database()
    
    # for num_of_doc in range(num_of_docs):
    database.add_to_db(num_of_docs)

if __name__ == "__main__":
    load_dotenv()
    main()

