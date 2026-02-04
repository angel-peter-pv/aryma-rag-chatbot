import json
import os
import faiss
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI


class Retriever:
    def __init__(self,index_path,metadata_path,embedding_model="text-embedding-3-small",top_k=5):
        self.index_path=index_path
        self.metadata_path=metadata_path
        self.embedding_model=embedding_model
        self.top_k=top_k
        self.client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.index=self._load_index()
        self.metadata = self._load_metadata()

    #to load faiss index from disk
    def _load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"FAISS index not found at {self.index_path}")
        return faiss.read_index(self.index_path)
    
    #load corresponding metadata
    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found at {self.metadata_path}")
        with open(self.metadata_path,"r",encoding="utf-8") as f:
            return json.load(f)
    
    #to convert query vector to embedding
    def _embed_query(self,query:str):
        response=self.client.embeddings.create(model=self.embedding_model,input=query)
        embedding=response.data[0].embedding
        return np.array([embedding], dtype="float32")
    
    #to retrieve top k docs relevant to query
    def retrieve(self,query):
        query_embedding=self._embed_query(query)
        distance, indices=self.index.search(query_embedding,self.top_k)

        results=[]
        for idx in indices[0]:
            if idx<len(self.metadata):
                results.append(self.metadata[idx])

        return results


if __name__ == "__main__":
    retriever = Retriever(index_path="data/faiss/index.bin",metadata_path="data/faiss/metadata.json",top_k=3)
    query = "What does Aryma Labs do?"
    docs = retriever.retrieve(query)

    print("\nRetrieved documents:\n")
    for doc in docs:
        print("URL:", doc.get("url"))
        print(doc.get("text", "")[:300])
        print()