from crawler import WebsiteCrawler
from change_detector import ChangeDetector
from chunker import Chunker
from embedder import Embedder
from index_manager import IndexManager

#Crawl, Change Detection,Chunking, Embedding, Indexing


def run_ingestion():

    BASE_URL = "https://arymalabs.com"

    #  Crawl website
    crawler = WebsiteCrawler(base_url=BASE_URL)
    crawled_pages = crawler.crawl(BASE_URL)
    print(f"Crawled pages: {len(crawled_pages)}")


    if not crawled_pages:
        print("No pages crawled.")
        return

    #  Detect changes
    change_detector = ChangeDetector(metadata_path="data/metadata.json")
    changes = change_detector.detect_change(crawled_pages)

    new_pages = changes["new"]
    updated_pages = changes["updated"]
    unchanged_pages = changes["unchanged"]

    print(f"New pages: {len(new_pages)}")
    print(f"Updated pages: {len(updated_pages)}")
    print(f"Unchanged pages: {len(unchanged_pages)}")

    # Update metadata ALL pages
    change_detector.update_metadata(new_pages + updated_pages + unchanged_pages)

    # Process only new & updated pages
    pages_to_process = new_pages + updated_pages

    if not pages_to_process:
        print("No new or updated pages to process.")
        return

    #  Chunk pages
    chunker = Chunker()
    chunks = chunker.chunk_pages(pages_to_process)
    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks generated.")
        return

    #  Embed chunks
    embedder = Embedder()
    embedded_chunks = embedder.embed_chunks(chunks)
    print(f"Chunks embedded: {len(embedded_chunks)}")

    if not embedded_chunks:
        print("No embeddings generated.")
        return

    #  Add embeddings to FAISS and save index
    index_manager = IndexManager()
    index_manager.add_embeddings(embedded_chunks)
    index_manager.save()

    print("Ingestion pipeline completed.")



if __name__ == "__main__":
    run_ingestion()
