import csv
import re
import os
import json
import time
import pandas as pd

from html import unescape
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.robotparser import RobotFileParser

from morizon_crawler import create_file_param

def unpack_property_details(details, separator="\n"):
    splitted_list = list(details.split(separator))
    property_type = splitted_list.pop(0)
    splitted_list.remove('Budynek')
    splitted_list.remove('Kredyt')
    splitted_list.remove('Ogłoszenie')
    #create variables with values
    #Type: FLAT
    standard = splitted_list[1]
    total_area = splitted_list[3]
    height = splitted_list[5]
    level = splitted_list[7]
    no_levels = splitted_list[9]
    kitchen_type = splitted_list[11]
    market_type = splitted_list[13]
    ownership_form = splitted_list[15]
    #Type: BULDING
    bulding_type = splitted_list[17]
    material = splitted_list[19]
    year = splitted_list[21]
    heating = splitted_list[23]
    #Type: OFFER
    date_added = splitted_list[25]
    update = splitted_list[27]
    offer_number = splitted_list[29]
    no_views = splitted_list[31]
    no_conquest = splitted_list[33]                                                                   
    return property_type, standard, total_area, height, level, no_levels, kitchen_type, market_type, ownership_form, bulding_type, material, year, heating, date_added, update, offer_number, no_views, no_conquest

def clean_text(text):
    cleaned_text = text.replace("\n", " ") 
    return cleaned_text

def main():
    current_dir = os.getcwd()

    prop_offer_links = pd.read_csv(f'{current_dir}/data/links/test.cvs')
    #prop_offer_links = pd.read_csv('../morizon/data/links/Morizon_links14-08-2023_18_44.csv')
    options = Options()
    #options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 2)

    robot_parser = RobotFileParser()
    robot_parser.set_url('https://www.morizon.pl/robots.txt')
    robot_parser.read()

    base_filename, full_path = create_file_param('bases')

    with open(f'{full_path}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'row_price', 'row_price_m2', 'main_location', 'property_type', 'standard', 'total_area', 'height', 'level', 'no_levels', 'kitchen_type', 'market_type', 'ownership_form', 'bulding_type', 'material', 'year', 'heating', 'date_added', 'update', 'offer_number', 'no_views', 'no_conquest', 'facilities', 'media', 'description'])

        property_details_list = []
        error_number = 0
        added_number = 1

        for index, offer in enumerate(prop_offer_links.iloc[:, 0]):
            try:
                #Open offer
                id = offer[-10:]
                print(offer)
                driver.get(offer)
                #Try to click pop-up
                try:
                    pop_button = driver.find_element(By.CSS_SELECTOR, 'button.cmp-button_button:nth-child(2)')
                    pop_button.click()
                except NoSuchElementException:
                    pass

                button = driver.find_element(By.CSS_SELECTOR, f"#mzn{id} > div > div:nth-child(3) > div > div > div.basic-info > div.basic-info__description-container > div > div.button__wrapper > button")
                driver.execute_script("arguments[0].scrollIntoView();", button)

                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()

                description = driver.find_element(By.CSS_SELECTOR, "span.description-text").text
                row_price = driver.find_element(By.CSS_SELECTOR, "#basic-info-price-row > div > span.price-row__price").text
                row_price_m2 = driver.find_element(By.CSS_SELECTOR, "#basic-info-price-row > div > span.price-row__price-m2").text
                main_location = driver.find_element(By.CSS_SELECTOR, "span.main-location").text
                detailed_information = driver.find_element(By.CSS_SELECTOR, f"#mzn{id} > div > div:nth-child(3) > div > div > div:nth-child(3) > div").text
                facilities = driver.find_element(By.CSS_SELECTOR, f"#mzn{id} > div > div:nth-child(3) > div > div > div:nth-child(4) > ul > li").text
                media = driver.find_element(By.CSS_SELECTOR, f"#mzn{id} > div > div:nth-child(3) > div > div > div:nth-child(5) > ul > li").text

                property_type, standard, total_area, height, level, no_levels, kitchen_type, market_type, ownership_form, bulding_type, material, year, heating, date_added, update, offer_number, no_views, no_conquest = unpack_property_details(detailed_information)

                property_details = {
                    'id': id,
                    'row_price': row_price,
                    'row_price_m2': row_price_m2,
                    'main_location': main_location,
                    'property_type': property_type,
                    'standard': standard,
                    'total_area': total_area,
                    'height': height,
                    'level': level,
                    'no_levels': no_levels,
                    'kitchen_type': kitchen_type,
                    'market_type': market_type,
                    'ownership_form': ownership_form,
                    'bulding_type': bulding_type,
                    'material': material,
                    'year': year,
                    'heating': heating,
                    'date_added': date_added,
                    'update': update,
                    'offer_number': offer_number,
                    'no_views': no_views,
                    'no_conquest': no_conquest,
                    'facilities': facilities,
                    'media': media,
                    'description': description
                }

                property_details_list.append(property_details)

                print(f'Offer {id} added to base, it was #{added_number}')
                added_number += 1

                if index % 10 == 0:
                    with open(f'{base_filename}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(property_details_list, json_file, ensure_ascii=False)

            except NoSuchElementException:
                error_number += 1
                print(f'Error number: {error_number} Offer id: {id}')
            except TimeoutException:
                print(f'Timeout error for offer id: {id}')
            
            except Exception as exc:
                print(exc)
                print(f'@@@@@ {exc} in {id}')
            finally:
                with open(f'{base_filename}.json', 'w', encoding='utf-8') as json_file:
                    json.dump(property_details_list, json_file, ensure_ascii=False)
        driver.quit()

if __name__ == "__main__":
    main()