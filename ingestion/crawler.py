import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
from typing import Set 
import re

#crawls, extract clean text, returns structed data
class WebsiteCrawler:
    def __init__(self,base_url):
        self.base_url= base_url
        self.domain= urlparse(base_url).netloc
        self.visited_urls:Set[str]= set()
    
    #take raw html content
    def fetch_page(self,url):  
        headers = {
                    "Host": "arymalabs.com",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/144.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                            "image/avif,image/webp,image/apng,*/*;q=0.8,"
                            "application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"macOS"',
                    "Accept-Encoding": "gzip, deflate, br",
                    "Priority": "u=0, i",
                    "Connection": "keep-alive"
                    }

        try:
            response= requests.get(url,headers=headers,timeout=10,allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            # print("Request failed:", e)
            return ""

    # to convert raw html to text
    def clean_html(self,html):
        soup= BeautifulSoup(html,"html.parser")

        for tag in soup(["script","style","nav","footer","header"]):
            tag.decompose()
        
        #extract visible text and normalize whitespace
        text= soup.get_text(separator=" ")
        text=" ".join(text.split())

        # remove emojis 
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F" 
            "\U0001F300-\U0001F5FF"  
            "\U0001F680-\U0001F6FF"  
            "\U0001F700-\U0001F77F"  
            "\U0001F780-\U0001F7FF" 
            "\U0001F800-\U0001F8FF"  
            "\U0001F900-\U0001F9FF"  
            "\U0001FA00-\U0001FAFF"  
            "\u2600-\u26FF"          
            "\u2700-\u27BF"          
            "]+",
            flags=re.UNICODE
        )

        text = emoji_pattern.sub("", text)
        return text
    
    #takes  all internal links from the current page.
    def extract_internal_links(self,html,current_url):
        soup = BeautifulSoup(html,"html.parser")
        links= set()
        for tag_a in soup.find_all("a",href=True):
            href =tag_a["href"]
            full_url=urljoin(current_url,href)
            parsed=urlparse(full_url)

            # keep only links belonging to the same domain
            if parsed.netloc==self.domain:
                links.add(full_url.split("#")[0])
        return links
    
    #generate hash
    def generate_hash(self,text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    

    def crawl(self,start_url):
        results=[]
        to_visit={start_url}

        while to_visit:
            url=to_visit.pop()
            

            ext=url.split(".")[-1]
            # skip these media file types
            unwanted=["mp3","mp4","jpeg","jpg","svg","pdf"]
        
            if (url in self.visited_urls ) or (ext in unwanted) :
                continue
            
            print("Crawling:", url)
            self.visited_urls.add(url)

            html=self.fetch_page(url)

            if not html:
                continue

            clean_text=self.clean_html(html)
            content_hash=self.generate_hash(clean_text)

            results.append({"url":url, "text": clean_text, "content_hash": content_hash})
            
            #new internal links taken and add unvisited URLs to queue
            internal_links=self.extract_internal_links(html,url)
            to_visit.update(internal_links-self.visited_urls)
        return results



        
if __name__ == "__main__":
    crawler = WebsiteCrawler("https://arymalabs.com")
    results = crawler.crawl("https://arymalabs.com")
    print(results)



