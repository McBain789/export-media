import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_media_links(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Warten auf das Laden der Seite
        
        media_links = {
            'videos': [],
            'audio': [],
            'streams': []
        }
        
        # Streams (z. B. m3u8 oder mpd) extrahieren
        sources = driver.find_elements(By.TAG_NAME, 'source')
        for source in sources:
            src = source.get_attribute('src')
            if src and ('.m3u8' in src or '.mpd' in src):
                media_links['streams'].append(urljoin(url, src))
        
        # Videos extrahieren
        videos = driver.find_elements(By.TAG_NAME, 'video')
        for video in videos:
            src = video.get_attribute('src')
            if src:
                media_links['videos'].append(urljoin(url, src))
        
        # Audio-Dateien extrahieren
        audios = driver.find_elements(By.TAG_NAME, 'audio')
        for audio in audios:
            src = audio.get_attribute('src')
            if src:
                media_links['audio'].append(urljoin(url, src))
        
    except Exception as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        media_links = None
    
    driver.quit()
    return media_links

if __name__ == "__main__":
    website_url = input("Gib die URL der Webseite ein: ")
    media = get_media_links(website_url)
    
    if media:
        print("Gefundene Medien:")
        for category, links in media.items():
            print(f"\n{category.capitalize()}:")
            for link in links:
                print(link)
