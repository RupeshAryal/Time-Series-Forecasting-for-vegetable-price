from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta

from tqdm import tqdm

import parser

# Set up the WebDriver
class BrowserInteraction:
    def __init__(self, driver=webdriver.Chrome()):
        self.driver = driver
        self.search_button_xpath = '/html/body/div[2]/main/div/div/div/div[1]/div/div/div/div/form/div/div[2]/button'
        self.date_input_xpath = '//*[@id="datePricing"]'
        self.menu_bar_xpath = '/html/body/header/div[3]/div/div/nav/ul/li[7]/a'
        self.language_dropdown_xpath = '/html/body/header/div[3]/div/div/nav/ul/li[7]/ul/div/a'
        self.url = url = 'https://kalimatimarket.gov.np/price#'

    def open_url(self):
        self.driver.get(self.url)
        self.driver.fullscreen_window()

    def change_language(self):
        menu = self.driver.find_element(By.XPATH, self.menu_bar_xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(menu).perform()

        dropdown_option = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH,self.language_dropdown_xpath))
        )
        dropdown_option.click()

    def get_page_source(self):
        date_input = self.driver.find_element(By.XPATH, self.date_input_xpath)
        date_input.send_keys(date.strftime('%m/%d/%Y'))

        search_button = self.driver.find_element(By.XPATH, self.search_button_xpath)
        search_button.click()

        return self.driver.page_source

    
# Define the start date
with open('last_extract_date.txt', 'r') as file:
    last_updated_date = file.read()
    start_date = datetime.strptime(last_updated_date, '%m/%d/%Y')

current_date = datetime.strftime(datetime.today(), '%m/%d/%Y')

print(current_date, last_updated_date)
if current_date == last_updated_date:
    print("The date has already been scrapped")

else:
    # Create a list to hold the dates
    delta = end_date = datetime.today() - start_date

    date_list = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    progress_bar = tqdm(total=len(date_list), desc=f"Progress")

    interaction = BrowserInteraction()
    interaction.open_url()
    interaction.change_language()

    for date in date_list:    
        source = interaction.get_page_source()
        
        _parser = parser.Parser(source, date.strftime("%m-%d-%Y"))
        _parser.table_extract()
        last_updated_date = date.strftime("%m/%d/%Y")


    with open('last_extract_date.txt', 'w') as file:
        file.write(last_updated_date)

    progress_bar.close()
        
    interaction.driver.quit()
