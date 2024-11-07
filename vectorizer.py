from sentence_transformers import SentenceTransformer

model_id = "sentence-transformers/all-MiniLM-L6-v2"

class Vectorizer:
    def __init__(self):
        self.model = SentenceTransformer(model_id)

    def vectorize(self, text):
        return self.model.encode(text)
    


###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"