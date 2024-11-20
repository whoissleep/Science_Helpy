import fitz
from tqdm import tqdm
from spacy.lang.en import English
import re
import pandas as pd
from vectorizer import Vectorizer

def formatting_text(text: str) -> str:
    return text.replace('\n', ' ').strip()

def split_list_of_text_into_chunks(slice_size: int, input_list: list) -> list:
    return [input_list[i: i + slice_size] for i in range(0, len(input_list), slice_size)]

def sentenize_text(pdfs_text: str) -> list:
    """
    Splits the input PDF text into individual sentences and calculates the number of sentence chunks.

    This function uses the spaCy library to tokenize and split the input text into sentences. It
    returns a list of sentences and the total number of sentence chunks.

    :param pdfs_text: The text extracted from a PDF document.
    :return: A tuple containing two dictionaries:
             - 'pdfs_text': A list of string sentences from the input text.
             - 'num_of_chunks': The number of sentence chunks.
    """
    nlp = English()
    nlp.add_pipe("sentencizer")
    pdfs_text = list(nlp(pdfs_text).sents)
    pdfs_text = [str(sent) for sent in pdfs_text]
    num_of_chunks = len(pdfs_text)

    pdfs_text_dict = {"pdfs_text": pdfs_text}
    num_of_chunks_dict = {"num_of_chunks": num_of_chunks}

    return pdfs_text_dict, num_of_chunks_dict
        
def read_and_preprocc_some_text(path_to_pdf: str, num_of_chunks: int=5) -> list[dict]:
    """
    This function reads a given PDF file and preprocesses its text into
    a list of dictionaries. Each dictionary contains information about a
    chunk of text in the PDF file, including the page number, the text
    itself, the number of tokens in the chunk, and the number of sentences
    in the chunk.

    The function returns a list of dictionaries, where each dictionary
    represents a chunk of text in the PDF file.

    :param path_to_pdf: The path to the PDF file to be read and preprocessed.
    :param num_of_chunks: The number of chunks to split the text into.
    :return: A list of dictionaries, where each dictionary represents a chunk
             of text in the PDF file. The list contains the following keys:
                - page_number: The page number of the chunk.
                - sents_chunks: The text of the chunk.
                - chunk_token_count: The number of tokens in the chunk.
    """
    pdf = fitz.open(path_to_pdf)
    all_info_of_pdf = []
    pdf_chunks = []

    for number_of_page, page in tqdm(enumerate(pdf)):
        text = formatting_text(page.get_text()).lower()
        all_info_of_pdf.append({
            "page_number": number_of_page,
            "page_word_counts": len(text.split(" ")),
            "page_sents_counts": len(text.split(". ")),
            "text": text,
            "sents": sentenize_text(text),
            "sents_chunks": split_list_of_text_into_chunks(num_of_chunks, sentenize_text(text)[0]["pdfs_text"]),
            "num_chunks": sentenize_text(text)[1]["num_of_chunks"]
        })

    for _, pdf_info in enumerate(all_info_of_pdf):
        for chunk in pdf_info['sents_chunks']:
            dict_of_pdf_info = {}
            dict_of_pdf_info['page'] = pdf_info['page_number']

            joined_sent_chunk = " ".join(chunk).replace("  ", " ").strip()
            joined_sent_chunk = re.sub(r'\.([A-Z])', r'. \1', joined_sent_chunk)

            dict_of_pdf_info['sents_chunks'] = joined_sent_chunk
            dict_of_pdf_info['chunk_token_count'] = len(joined_sent_chunk) / 4

            pdf_chunks.append(dict_of_pdf_info)

    df = pd.DataFrame(pdf_chunks)
    min_token_length = 50

    pdf_chunks = df[df['chunk_token_count'] > min_token_length].to_dict(orient='records')


    return pdf_chunks

def add_vectors_to_chunks(pdf_chunks: list[dict]) -> list[dict]:
    vectorizer = Vectorizer()
    df = pd.DataFrame(pdf_chunks)

    df['vectors'] = df['sents_chunks'].apply(lambda x: vectorizer.vectorize(x))
    
    pdf_chunks = df.to_dict(orient='records')

    return pdf_chunks


###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"
    