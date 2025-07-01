import re
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from readability import Document

class ArticleScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.options = chrome_options
        self.driver = None

    def __enter__(self):
        print("Starting Chrome WebDriver...")
        self.driver= webdriver.Chrome(options=self.options)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            print("Quitting Chrome WebDriver...")
            self.driver.quit()

    def scrape_article(self, url:str)->dict|None:
        if not self.driver:
            raise RuntimeError("WebDriver is not initialized. Use 'with' statement to manage the WebDriver context.")
        print(f"Scraping article from {url}...")
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            doc = Document(page_source)
            title = doc.title()
            content_html = doc.summary()
            soup = BeautifulSoup(content_html, 'html.parser')
            content_text = soup.get_text(separator="\n", strip=True)

            if not content_text:
                print("Readability could not find meaningful content.")
                return None

            return {"title": title, "content": content_text}

        except Exception as e:
            print(f"An error occurred during scraping {url}: {e}")
            return None
    def crawl_source(self, base_url: str, max_articles: int = 10) -> list[dict]:
        if not self.driver:
            raise RuntimeError("WebDriver is not initialized. Use 'with' statement to manage the WebDriver context.")
        print(f"Starting crawl from base URL: {base_url}")
        try:
            self.driver.get(base_url)
            page_source=self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            article_links = set()
            base_netloc= urlparse(base_url).netloc
            article_pattern = re.compile(r'https?://(?:www\.)?[^/]+/[^/]+/[^/]+/[^/]+')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if article_pattern.match(href):
                    full_url = urljoin(base_url, href)
                    if urlparse(full_url).netloc == base_netloc:
                        article_links.add(urljoin(full_url,urlparse(full_url).path))
                if len(article_links)>= max_articles:
                    break
            print(f"Found {len(article_links)} article links.")

            scraped_articles = []
            for links in list(article_links):
                article_data=self.scrape_article(links)
                if article_data:
                    scraped_articles.append(article_data)
            return scraped_articles
        except Exception as e:
            print(f"An error occurred during crawling {base_url}: {e}")
            return []