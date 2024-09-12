from bs4 import BeautifulSoup
import csv

class Parser:
    def __init__(self,source, date):
        self.source = source
        self.date = date
        self.soup = BeautifulSoup(source, 'html.parser')

    def table_extract(self):
        soup = self.soup
        table = soup.find_all('table')[1]
        rows = table.find_all('tr')

        with open(f"sample/{self.date}.csv", 'w',  newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            column = ['commodities', 'unit', 'minimum', 'maximum', 'average' ]
            csvwriter.writerow(column)

            for row in rows:
                cell = [x.get_text() for x in row.find_all('td')]
                    
                csvwriter.writerow(cell)



        


    

