from download_pdf import download_all_papers
from read_and_preprocc_pdf import read_and_preprocc_some_text, READY_add_vectors_to_chunks
from database import PostgreDB
from vectorizer import Vectorizer
from model_api import ChatModel
from dotenv import load_dotenv
import os

def main():
    path_to_pdfs = "/home/whoissleep/Документы/VS_CODE/proj/pdfs"
    api_key = os.getenv("HF_API")
    model_id = "Qwen/Qwen2.5-72B-Instruct"
    vectorizer = Vectorizer()
    chat_model = ChatModel(api_key=api_key, model_id=model_id)
    database = PostgreDB(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
    download_all_papers()
    database.create_database()
    num_of_docs = len(os.listdir(path_to_pdfs))
    
    pdf = read_and_preprocc_some_text("/home/whoissleep/Документы/VS_CODE/proj/pdfs/1.pdf")

    pdf = READY_add_vectors_to_chunks(pdf)

    print(pdf[0].keys())


if __name__ == "__main__":
    load_dotenv()
    main()

