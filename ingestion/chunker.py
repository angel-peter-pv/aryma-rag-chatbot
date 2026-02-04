#Split page text into overlapping character based chunks,
#Preserve URL and metadata
#Return chunks for embedding

class Chunker:
    def __init__(self,chunk_size = 800,overlap = 100,min_chars = 200):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chars = min_chars


    def _make_chunks(self, text) :
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]

            #discard small chunks
            if len(chunk) >= self.min_chars:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - self.overlap
        return chunks


    def chunk_pages(self, pages):

        all_chunks = []

        for page in pages:
            url = page["url"]
            text = page["text"].strip()
            content_hash = page["content_hash"]
            
            if len(text) < self.min_chars:
                continue


            text_chunks = self._make_chunks(text)

            for idx, chunk_text in enumerate(text_chunks):
                chunk = {
                    "chunk_id": f"{url}::chunk_{idx}", #created Unique ID combining source URL and chunk index for traceability and safe re-indexing
                    "url": url,
                    "text": chunk_text,
                    "content_hash": content_hash,
                }
                all_chunks.append(chunk)

        return all_chunks








if __name__ == "__main__":

    sample_pages = [
        {
            "url": "https://example.com/about",
            "text": "Aryma Labs builds AI systems. " * 200,
            "content_hash": "hash_123",
        }
    ]

    chunker = Chunker()
    chunks = chunker.chunk_pages(sample_pages)

    print(f"Total chunks created: {len(chunks)}\n")

    for chunk in chunks[:2]:
        print("Chunk ID:", chunk["chunk_id"])
        print("Character count:", len(chunk["text"]))
        print("Chunk text:")
        print(chunk["text"])

