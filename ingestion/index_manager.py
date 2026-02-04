import os
import json
import faiss
import numpy as np

# to handle storage and updating of vector embeddings using FAISS
class IndexManager:


    def __init__(self,index_path= "data/faiss/index.bin",metadata_path = "data/faiss/metadata.json",embedding_dim = 1536):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_dim = embedding_dim

        self.index = self._load_or_create_index()
        self.metadata = self._load_metadata()

    #to ensure faiss index always exists
    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatL2(self.embedding_dim)

    #to load chunk metadata aligned with faissvectors
    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            return []
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

    #to add new embeddings to faiss
    def add_embeddings(self, embedded_chunks):
        if not embedded_chunks:
            return
        
        vectors = np.array([chunk["embedding"] for chunk in embedded_chunks],dtype="float32")
        self.index.add(vectors)

        for chunk in embedded_chunks:
            self.metadata.append({"chunk_id": chunk["chunk_id"],"url": chunk["url"],"text": chunk["text"]})



    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path) #  to save the FAISS index to disk

        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)





if __name__ == "__main__":

    fake_embeddings = [
        {
            "chunk_id": "test::chunk_0",
            "url": "https://example.com",
            "text": "Sample chunk text one.",
            "embedding": np.random.rand(1536).astype("float32").tolist(),
        },
        {
            "chunk_id": "test::chunk_1",
            "url": "https://example.com",
            "text": "Sample chunk text two.",
            "embedding": np.random.rand(1536).astype("float32").tolist(),
        },
    ]

    manager = IndexManager()
    manager.add_embeddings(fake_embeddings)
    manager.save()

    print("FAISS index size:", manager.index.ntotal)
