from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
from .constants import PATH, URL

class JournalArticle:
    def __init__(self):
        search_term=input("Enter search term: ")
        self.search_term=search_term
        driver = webdriver.Chrome(service=Service(PATH))
        self.driver=driver
        self.driver.implicitly_wait(10)
        super(JournalArticle, self).__init__()

    def land_ncbi_page(self):
        self.driver.get(URL)
    
    def search(self):
        # search_term=input("Enter search term: ")
        # self.search_term=search_term
        search = self.driver.find_element(By.XPATH, '//input[@name="term"]')
        search.send_keys(self.search_term)
        # search.send_keys(search_term)
        search.send_keys(Keys.RETURN)

    def get_journal_info(self, journal):
        journal_title = journal.find_element(By.XPATH, './/a[@class="docsum-title"]').text
        journal_authors = journal.find_element(By.XPATH, './/span[@class="docsum-authors full-authors"]').text
        journal_journal = journal.find_element(By.XPATH, './/span[@class="docsum-journal-citation full-journal-citation"]').text
        journal_info = (journal_title, journal_authors, journal_journal)
        return journal_info

    def scrape_data(self):
        journal_ids = set()
        all_data = []
        self.all_data = all_data
        while True:
            journals = self.driver.find_elements(By.XPATH, '//article[@class="full-docsum"]')
            for journal in journals[-20:]:
                data = self.get_journal_info(journal)
                if data:
                    journal_id = ''.join(data)
                    if journal_id not in journal_ids:
                        journal_ids.add(journal_id)
                        all_data.append(data)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            try:
                self.driver.find_element(By.XPATH, '//button[@class="load-button next-page"]').click()
            except NoSuchElementException:
                if bool(all_data):
                    print("Scrapping Complete")
                else:
                    print("Your search term retrieved zero results")
                break
            sleep(2)
        self.driver.close()
        return all_data

    def save_data(self):
        if bool(self.all_data):
            with open(f"{self.search_term}_journals.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                header = ['Title', 'Authors', 'Journal']
                writer.writerow(header)
                writer.writerows(self.all_data)
