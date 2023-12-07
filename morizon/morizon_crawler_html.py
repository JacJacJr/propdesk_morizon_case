import time
import csv
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def get_max_pages_manually():
    while True:
        try:
            pages = int(input("Enter the maximum number of pages to scrape (integer value): "))
            if pages < 0:
                print("Please enter a positive integer greater than zero, or 0 to find maximum number of sites.")
            elif pages == 0:
                max_pages = get_max_pages()
                print(f'The number of all pages is {max_pages}')
                return max_pages
            else:
                return pages
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_max_pages():
    url = "https://www.morizon.pl/mieszkania/warszawa/"
    
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url)
        time.sleep(1)

        # Find the maximum number of pages in pagination
        max_pages_element = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[1]/section/div[5]/div/div[2]/div[6]/a/div/span')
        max_pages = int(max_pages_element.text)

        return max_pages

    except Exception as e:
        print(f"Error while processing the page: {e}")
        return 0

    finally:
        driver.quit()

def get_all_links(max_pages):
    base_url = "https://www.morizon.pl/mieszkania/warszawa/?page={}"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    all_links = []
    all_id = []

    try:
        for page_number in range(1, max_pages + 1):
            url = base_url.format(page_number)
            driver.get(url)
            time.sleep(1)

            # Extract links from the page source using regex
            link_pattern = r'href="/oferta/[^"]+"'
            links = re.findall(link_pattern, driver.page_source)

            for link in links:
                link_id = link[-13:-1]  # Extract the last 12 characters of the link
                if link_id not in all_id:
                    all_id.append(link_id)
                    full_link = "https://www.morizon.pl" + link[6:-1]  # Extract the URL
                    all_links.append(full_link)

            # Print current page number
            print(f"Processing page {page_number}...")

    except Exception as exc:
        print(f"Error while processing the page: {exc}")

    finally:
        driver.quit()

    return all_links

def run_crawler():
    # Ask user for the maximum number of pages
    max_pages = get_max_pages_manually()

    # Get the maximum number of pages in pagination if not provided by the user
    if max_pages <= 0:
        max_pages = get_max_pages()

    if max_pages > 0:
        # Get all the links from the pages
        all_links = get_all_links(max_pages)

        #Generating filname with curent date and time
        #todo: add this file version to dictionary data/links
        filename = f'Morizon_links:{datetime.now().strftime("%d%m%Y__%H_%M")}'
        # Save all the links to a CSV file
        with open(f'data/links/{filename}.csv', "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Links"])
            writer.writerows([[link] for link in all_links])

if __name__ == "__main__":
    run_crawler()
