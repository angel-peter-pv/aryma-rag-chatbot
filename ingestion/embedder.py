import os
from openai import OpenAI

# converts text chunks into vector embeddings
class Embedder:

    def __init__(self, model = "text-embedding-3-small",):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_chunks(self, chunks):
        texts = [chunk["text"] for chunk in chunks]

        if not texts:
            return []

        response = self.client.embeddings.create(model=self.model,input=texts,)
        embedded_chunks = []


        for chunk, embedding_data in zip(chunks, response.data):
            #copy the original chunk data and add the embedding vector
            embedded_chunk = {**chunk,"embedding": embedding_data.embedding}
            embedded_chunks.append(embedded_chunk)

        return embedded_chunks





if __name__ == "__main__":

    sample_chunks = [
        {
            "chunk_id": "test::chunk_0",
            "url": "https://example.com",
            "text": "Aryma Labs builds AI systems for modern enterprises.",
            "content_hash": "hash_123",
        },
        {
            "chunk_id": "test::chunk_1",
            "url": "https://example.com",
            "text": "Their focus includes applied AI, agents, and scalable ML systems.",
            "content_hash": "hash_123",
        },
    ]

    embedder = Embedder()
    embedded = embedder.embed_chunks(sample_chunks)

    print(f"Chunks embedded: {len(embedded)}\n")

    for c in embedded:
        print("Chunk ID:", c["chunk_id"])
        print("Embedding length:", len(c["embedding"]))

