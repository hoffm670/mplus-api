import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import random



# a = webdriver.ChromeService('/home/hoffm670/repos/mplus-python/chromedriver')  # Optional argument, if not specified will search path.
driver = webdriver.Chrome()


# time.sleep(5) # Let the user actually see something!

# for i in range(0, 50):
    
#     driver.get(f'https://raider.io/mythic-plus-character-rankings/season-df-3/us/all/all/{i}')
#     print(f'{i}')
#     time.sleep(random.uniform(5, 10)) # Let the user actually see something!


driver.get(f'https://raider.io/mythic-plus-character-rankings/season-df-3/us/all/all/2')


# /html/body/div[2]/div[6]/div[3]/div[2]/div/div[2]/div/div[1]/div[3]/table/tbody/tr[2]/td[2]/div/div/span/span/span/a
#content > div > div.slds-col.slds-size--1-of-1 > div.fresnel-container.fresnel-greaterThan-sm > table > tbody > tr:nth-child(2) > td.slds-text-align--left > div > div > span
# table = driver.find_elements_by_tag_name('table')
span = driver.find_elements(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > span')
character = span[0].text

div = driver.find_elements(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > div')
server = div[0].text
# print(table[0])
# actions = ActionChains(driver)
print(character)
print(server)

time.sleep(100)
driver.quit()