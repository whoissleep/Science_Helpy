import faiss
import pandas as pd
import numpy as np
from database import PostgreDB
from vectorizer import Vectorizer
from dotenv import load_dotenv

load_dotenv()

class RAG:
    def __init__(self, database: PostgreDB, vectorizer: Vectorizer):
        self.database = database
        self.vectorizer = vectorizer

    def return_context(self, text: str):
        data = pd.DataFrame(self.database.fetch_data())
        vec_of_text = self.vectorizer.vectorize(text)
        vectors = np.array(data[1].tolist()).astype('float32')
        dimension = vectors.shape[1]
        index = faiss.IndexFlatIP(dimension)

        index.add(vectors)

        vec_of_text_np = np.array([vec_of_text]).astype('float32')

        distances, indices = index.search(vec_of_text_np, k=5)

        # for i, idx in enumerate(indices[0]):
        #     print(f"Document {idx}: Distance = {distances[0][i]}")
        #     print(f"Text {idx}: {data[0].iloc[idx]}")
        
        result = []
        for i in range(len(indices[0])):
            rag_text = list(data[0].iloc[[indices[0][i]]])[0]
            result.append(rag_text[0])

        return result