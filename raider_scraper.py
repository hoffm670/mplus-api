import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from constants import RAIDER_RANKINGS_URL, PAGE_SIZE, ROW_CLASS, CHARACTER_SELECTOR, SERVER_SELECTOR, SERVER_REGEX
import random
import re

logger = logging.getLogger('raider.scraper')

class RaiderScraper:
    
    def __init__(self) -> None:
        options = Options()
        options.add_argument('--headless=true')
        self.driver = webdriver.Chrome(options=options)
        
    def get_title_players(self, num_eligible, season, region):
        toons = []
        page_number = 0
        remaining = num_eligible
        while remaining > 0:
            logger.debug(f'{RAIDER_RANKINGS_URL}/{season}/{region}/all/all/{page_number}')
            logger.info(f'Parsing raider.io page {page_number}')
            self.driver.get(f'{RAIDER_RANKINGS_URL}/{season}/{region}/all/all/{page_number}')
            
            all_rows = self.driver.find_elements(By.CLASS_NAME, ROW_CLASS)
            if len(all_rows) != PAGE_SIZE:
                raise Exception(f'Scraping failed. Page Size: {PAGE_SIZE} Rows Found: {len(all_rows)}')
            
            for i in range(0, min(PAGE_SIZE, remaining)):
                base = all_rows[i]
                
                span = base.find_elements(By.CSS_SELECTOR, CHARACTER_SELECTOR)
                name = span[0].text
                
                div = base.find_elements(By.CSS_SELECTOR, SERVER_SELECTOR)
                region, server = re.search(SERVER_REGEX, div[0].text).groups()
                
                if server != 'Anonymous':
                    toons.append({"name": name, "server": server, "region": region})
                remaining-=1
            page_number+=1
            
            # Don't get caught
            time.sleep(random.uniform(5, 10)) 
        return toons