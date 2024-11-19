from download_pdf import download_all_papers
from database import PostgreDB
from vectorizer import Vectorizer
from model_api import ChatModel
from dotenv import load_dotenv
import os
from tqdm.auto import tqdm
import pandas as pd
from RAG import RAG

def main():
    path_to_pdfs = "/home/whoissleep/Документы/VS_CODE/proj/pdfs"
    num_of_docs = len(os.listdir(path_to_pdfs))
    api_key = os.getenv("HF_API")
    model_id = "Qwen/Qwen2.5-72B-Instruct"
    chat_model = ChatModel(api_key=api_key, model_id=model_id)
    vectorizer=Vectorizer()
    database = PostgreDB(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
    download_all_papers()
    database.create_database()
    
    if database.count_values() == 0:
        database.add_to_db(num_of_docs)

    rag = RAG(database=database, vectorizer=vectorizer)
    context = rag.return_context(text="Attention is all you need")
#TODO добавить текст из рага в ллмку и сделать вывод

if __name__ == "__main__":
    load_dotenv()
    main()