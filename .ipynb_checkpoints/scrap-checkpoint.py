from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

import os
from tqdm import tqdm

import parser

# Set up the WebDriver
class BrowserInteraction:
    def __init__(self, driver):
        self.driver = webdriver.Chrome()
        self.search_button_xpath = '/html/body/div[2]/main/div/div/div/div[1]/div/div/div/div/form/div/div[2]/button'
        self.date_input_xpath = '//*[@id="datePricing"]'

    def get_page_source(self, driver):
        


driver = webdriver.Chrome()


url = 'https://kalimatimarket.gov.np/price#'

driver.get(url)
driver.fullscreen_window()
#The following lines of codes change the language of the website

menu = driver.find_element(By.XPATH, '/html/body/header/div[3]/div/div/nav/ul/li[7]/a')
actions = ActionChains(driver)
actions.move_to_element(menu).perform()

dropdown_option = WebDriverWait(driver, 4).until(
    EC.visibility_of_element_located((By.XPATH,'/html/body/header/div[3]/div/div/nav/ul/li[7]/ul/div/a' ))
)
dropdown_option.click()


# Define the start date
start_date = datetime.strptime('01/01/2014', '%m/%d/%Y')


# Create a list to hold the dates
date_list = [start_date + timedelta(days=i) for i in range(3865)]

progress_bar = tqdm(total=len(date_list), desc=f"Progress")

for date in date_list:
    date_input = driver.find_element(By.XPATH, '//*[@id="datePricing"]')
    date_input.send_keys(date.strftime('%m/%d/%Y'))

    search_button = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div/div[1]/div/div/div/div/form/div/div[2]/button')
    search_button.click()

    source = driver.page_source
    _parser = parser.Parser(source, date.strftime("%m-%d-%Y"))
    
    _parser.table_extract()

    progress_bar.update(1)

progress_bar.close()
    
driver.quit()



       
    


# html = driver.find_element(By.TAG_NAME, 'html')
# lang = driver.find_element(By.XPATH, '/html/body/header/div[3]/div/div/nav/ul/li[7]/ul/div/a')
# lang.click()
# new_lang = "en"
# driver.execute_script(f"arguments[0].setAttribute('lang', '{new_lang}')", html)
# print("Lang attribute changed")
