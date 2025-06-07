from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
from datetime import date


SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://standalone-chrome:4444/wd/hub")


options = Options()
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

class BrowserInteraction:
    def __init__(self):
        # self.driver = webdriver.Remote(SELENIUM_URL , DesiredCapabilities.CHROME, options=options)

        self.driver = webdriver.Chrome(options=options)
        self.search_button_xpath = '/html/body/div[2]/main/div/div/div/div[1]/div/div/div/div/form/div/div[2]/button'
        self.date_input_xpath = '//*[@id="datePricing"]'
        self.menu_bar_xpath = '/html/body/header/div[3]/div/div/nav/ul/li[7]/a'
        self.language_dropdown_xpath = '/html/body/header/div[3]/div/div/nav/ul/li[7]/ul/div/a'
        self.url = 'https://kalimatimarket.gov.np/price#'

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

    def get_page_source(self, date):
        date_input = self.driver.find_element(By.XPATH, self.date_input_xpath)
        date_input.send_keys(date.strftime('%m/%d/%Y'))

        search_button = self.driver.find_element(By.XPATH, self.search_button_xpath)
        search_button.click()

        return self.driver.page_source
