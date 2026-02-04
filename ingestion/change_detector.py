# ChangeDetector is responsible for identifying new, updated, and unchanged pages between crawls

import json
import os

class ChangeDetector:
    def __init__(self,metadata_path):
        self.metadata_path=metadata_path
        self.metadata=self._load_metadata()


    # loads previously stored url to hash metadata
    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            return {}

        if os.path.getsize(self.metadata_path) == 0:
            return {}

        try:
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        
            
    # to compare newly crawled pages with stored metadata to detect change
    def detect_change(self,crawled_data):
        new_pages = []
        updated_pages = []
        unchanged_pages = []

        for page in crawled_data:
            url=page["url"]
            new_hash=page["content_hash"]
            old_hash=self.metadata.get(url)

            if old_hash is None:
                new_pages.append(page)

            elif old_hash["content_hash"] != new_hash:
                updated_pages.append(page)

            else:
                unchanged_pages.append(page)

        return {"new":new_pages,"updated":updated_pages,"unchanged":unchanged_pages}    


    # to update metadata storage with the latest content hashes for all crawled pages
    def update_metadata(self, pages):
        for page in pages:
            self.metadata[page["url"]]={"text": page["text"],
                                        "content_hash": page["content_hash"],}
        
        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)

        with open (self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata,f,indent=2)




if __name__ == "__main__":
    crawled_data = [
        {
            "url": "https://example.com/page1",
            "text": "This is page one",
            "content_hash": "hash_1"
        },
        {
            "url": "https://example.com/page2",
            "text": "This is page two",
            "content_hash": "hash_2"
        }
    ]

    detector = ChangeDetector("data/metadata.json")
    changes = detector.detect_change(crawled_data)

    print("Detected changes:")
    print(changes)

    detector.update_metadata(changes["new"] + changes["updated"] + changes["unchanged"])
