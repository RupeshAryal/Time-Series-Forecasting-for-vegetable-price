from browser import BrowserInteraction
from parser import Parser

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


from datetime import datetime, timedelta
from tqdm import tqdm

def test_selenium_server_available():

    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:
        session.get("http://standalone-chrome:4444/wd/hub")
    except Exception as e:
        print("failed to start a connection")


test_selenium_server_available()


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

    for date in tqdm(date_list):    
        source = interaction.get_page_source(date)
        _parser = Parser(source, date.strftime("%m-%d-%Y"))
        _parser.table_extract()
        last_updated_date = date.strftime("%m/%d/%Y")


    with open('last_extract_date.txt', 'w') as file:
        file.write(last_updated_date)

    progress_bar.close()
        
    interaction.driver.quit()
