from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from readability import Document
from bs4 import BeautifulSoup

def scrape_article(url):
    # Set up Chrome options

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    # Initialize the WebDriver
    #CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver-linux64/chromedriver"
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        page_source = driver.page_source
        doc=Document(page_source)
        title= doc.title()
        content_html = doc.summary()
        soup= BeautifulSoup(content_html, 'html.parser')
        content_text = soup.get_text(separator="\n", strip=True)
        if not content_text:
            print("Readability could not find meaningful content.")
            return None

        return {"title": title, "content": content_text}

    except Exception as e:
        print(f"An error occurred during scraping {url}: {e}")
        return None

    finally:
        if driver:
            driver.quit()

