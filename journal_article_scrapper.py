# import required libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv


# prompts for search term
search_term = input('Enter search term: ')

# function that extracts title, authors and journal of the target articles


def get_journal_info(journal):
    journal_title = journal.find_element_by_xpath(
        './/a[@class="docsum-title"]').text
    journal_authors = journal.find_element_by_xpath(
        './/span[@class="docsum-authors full-authors"]').text
    journal_journal = journal.find_element_by_xpath(
        './/span[@class="docsum-journal-citation full-journal-citation"]').text
    journal_info = (journal_title, journal_authors, journal_journal)
    return journal_info


# load chrome drivers and create and its instance
# Full path to the chrome driver
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# navigates to pubmed website
driver.get('https://pubmed.ncbi.nlm.nih.gov/')


# finds search input and searches for provided search term
search = driver.find_element_by_xpath('//input[@name="term"]')
search.send_keys(search_term)
search.send_keys(Keys.RETURN)

# get all article's title, authors and journal
journal_ids = set()
all_data = []
while True:
    journals = driver.find_elements_by_xpath('//article[@class="full-docsum"]')
    for journal in journals[-20:]:
        data = get_journal_info(journal)
        if data:
            journal_id = ''.join(data)
            if journal_id not in journal_ids:
                journal_ids.add(journal_id)
                all_data.append(data)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    try:
        driver.find_element_by_xpath(
            '//button[@class="load-button next-page"]').click()
    except NoSuchElementException:
        if bool(all_data):
            print("Scrapping Complete")
        else:
            print("Your search term retrieved zero results")
        break
    sleep(2)
driver.close()

# writes the output data to csv file
if bool(all_data):
    with open(f"{search_term}_journals.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['Title', 'Authors', 'Journal']
        writer.writerow(header)
        writer.writerows(all_data)
