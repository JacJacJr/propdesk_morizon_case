import re
import csv
import json
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import regex_list as reg
import os
import traceback
from bs4 import BeautifulSoup

def save_to_dict(details_dict, key, variable):
    if variable is not None and variable != '' and variable != []:
        if type(variable) is int or type(variable) is str:
            # Change comma to other separator
            variable = str(variable).replace(',', ' ')
            variable = re.sub(reg.variable_html, '', variable)
            details_dict[key] = variable    
        elif type(variable) is list:
            variable = ' '.join(variable)
            variable = variable.replace(',', ' ')
            variable = re.sub(reg.variable_html, '', variable)
            variable = re.sub(reg.variable_white, ' ', variable).strip()
            details_dict[key] = variable  
        else: 
            details_dict[key] = 'n/a'
            print(f'Other type of viriable in save_to_dict in {key}')
    else:
        variable = 'NULL'
        details_dict[key] = variable

def extract_and_save_to_dict(source, regex_pattern, phrase, details_dict):
    result = re.findall(regex_pattern, source)
    save_to_dict(details_dict, phrase, result)

def set_flag_and_save_to_dict(source, keyword, property_name, details_dict):
    if keyword in source:
        flag = 1
    else:
        flag = 0
    save_to_dict(details_dict, property_name, flag)
    return flag 

# Get absolute path for the data directories
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'data', 'scrapped', 'json')
csv_path = os.path.join(current_dir, 'data', 'scrapped', 'csv')

# Create directories if they don't exist
os.makedirs(json_path, exist_ok=True)
os.makedirs(csv_path, exist_ok=True)

# Use absolute path for JSON and CSV files
filename = f'Morizon_data:{datetime.now().strftime("%d%m%Y_%H")}'
json_file_path = os.path.join(json_path, f'{filename}.json')
csv_file_path = os.path.join(csv_path, f'{filename}.csv')

# Get absolute path for the data directory
data_path = os.path.join(current_dir, 'data', 'links')

# Read CSV file using absolute path
csv_file = 'Morizon_links:26012025__12_29.csv'
file_path = os.path.join(data_path, csv_file)

# Make sure directory exists
os.makedirs(data_path, exist_ok=True)

# Read the CSV file
prop_offer_links = pd.read_csv(file_path)

options = Options()
options.add_argument('--headless') 
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(10)

error_no_element = 0
error_time_out = 0
error_another = 0
error_web_driver = 1
error_count = 0

progress_number = 1
added_number = 0
empty_link = 0 

start_time = time.time() 

try:
    for offer in prop_offer_links.iloc[:, 0]:
        try:
            error = False
            driver.get(offer)
            # Save whole html for processing
            source = driver.page_source

            # Check if the offer is still available
            phrases_to_check = ["którego szukasz, jest już nieaktualne", "Brak ofert spełniających Twoje kryteria", 
                              "Pod tym adresem nic nie ma...", "https://www.morizon.pl/_nuxt/error404.e3aeda20.svg"]
            if any(phrase in source for phrase in phrases_to_check):
                empty_link += 1
                continue 
            else:
                print(f'Progress: {progress_number}/{len(prop_offer_links)}\n {offer}')
                details_dict = {}       
                save_to_dict(details_dict, 'url', offer)     

                # Information from url 
                platform = re.findall(reg.platform, offer)
                save_to_dict(details_dict, 'platform', platform)

                link_content = re.findall(reg.link_content, offer)
                link_content = link_content[0] 
                link_parts = link_content.split('-')
                
                # Extract information from URL parts
                transaction_type = link_parts.pop(0)
                save_to_dict(details_dict, 'transaction_type', transaction_type)  

                property_type = link_parts.pop(0)
                save_to_dict(details_dict, 'property_type',property_type)            

                city = link_parts.pop(0)
                save_to_dict(details_dict, 'city', city)

                id = link_parts.pop(-1)
                save_to_dict(details_dict, 'id', id)  

                total_area = link_parts.pop(-1)[:-2]
                save_to_dict(details_dict,'total_area', total_area)

                # Process district information
                if len(link_parts) > 0:
                    district = link_parts.pop(0)
                    
                    two_word_district = ['polnoc', 'północ', 'południe', 'poludnie']
                    if any(word in link_parts for word in two_word_district):
                        district_secound_word = link_parts.pop(0)
                        district = district + ' ' + district_secound_word

                    if len(link_parts) == 0 or link_parts == ['']:
                        prec_adress = 'n/a'
                    else:
                        prec_adress = ' '.join(link_parts)
                else:
                    district = 'n/a'
                    
                save_to_dict(details_dict,'district', district)
                save_to_dict(details_dict,'prec_adress', prec_adress)

                #informations from html source
                #prices
                try:
                    price_container = driver.find_element(By.CSS_SELECTOR, "#basic-info-price-row > div")
                    price_spans = price_container.find_elements(By.CSS_SELECTOR, "span")
                    price_text = price_container.text
                    
                    # List of phrases indicating no specific price
                    no_price_phrases = ['ZAPYTAJ O CENĘ', 'Zapytaj o cenę', 'Zarezerwowano', 'zapytaj o cenę']
                    
                    if not price_spans or any(phrase in price_text for phrase in no_price_phrases):
                        row_price = "n/a"
                        row_price_m2 = "n/a"
                        primary_market = "n/a"
                    else:
                        prices = [span.get_attribute('innerHTML') for span in price_spans]
                        if prices and prices[0] and not any(phrase in prices[0] for phrase in no_price_phrases):
                            row_price = prices[0].strip()
                            row_price_m2 = prices[1].strip() if len(prices) > 1 and prices[1] else "n/a"
                            primary_market = row_price
                        else:
                            row_price = "n/a"
                            row_price_m2 = "n/a"
                            primary_market = "n/a"
                except NoSuchElementException:
                    print("Price source element not found!")
                    row_price = "n/a"
                    row_price_m2 = "n/a"
                    primary_market = "n/a"
                
                save_to_dict(details_dict,'row_price', row_price)
                save_to_dict(details_dict,'row_price_m2', row_price_m2)
                save_to_dict(details_dict,'primery_market', primary_market)

                #floors
                property_levels = re.findall(reg.property_levels, source)

                if property_levels:
                    try:
                        property_level, total_property_level = property_levels[0].split('/')
                    except ValueError:
                        print(f'No information about property_levels in {id}')
                else:
                    property_level = 'n/a'
                    total_property_level = 'n/a'

                save_to_dict(details_dict,'property_level', property_level)
                save_to_dict(details_dict,'total_property_level', total_property_level)

                #regex without split functions
                description = re.findall(reg.description_p, source, re.DOTALL)
                if description == []:
                    description = re.findall(reg.description_d, source, re.DOTALL)
                save_to_dict(details_dict,'description', description)

                extract_and_save_to_dict(source, reg.market_type, 'market_type', details_dict)
                extract_and_save_to_dict(source, reg.building_type, 'building_type', details_dict)
                extract_and_save_to_dict(source, reg.no_rooms, 'no_rooms', details_dict)
                extract_and_save_to_dict(source, reg.kitchen_type, 'kitchen_type', details_dict)
                extract_and_save_to_dict(source, reg.building_year, 'building_year', details_dict)
                extract_and_save_to_dict(source, reg.material, 'material', details_dict)
                extract_and_save_to_dict(source, reg.heating_type, 'heating_type', details_dict)
                extract_and_save_to_dict(source, reg.water, 'water', details_dict)

                # Check for additional property features
                set_flag_and_save_to_dict(source, ',"Winda",', 'elevator', details_dict)
                set_flag_and_save_to_dict(source, ',"Gaz",', 'gas', details_dict)
                set_flag_and_save_to_dict(source, '"Łazienka razem z WC","Tak"', 'bath_with_wc', details_dict)
                set_flag_and_save_to_dict(source, '="Prąd"', 'electricity', details_dict)
                set_flag_and_save_to_dict(source, 'parking_places', 'parking', details_dict)
                set_flag_and_save_to_dict(source, '>Piwnica<', 'basement', details_dict)
                balcony = set_flag_and_save_to_dict(source, '"Balkon","Tak"', 'balcony', details_dict)
                if balcony == 0:
                    set_flag_and_save_to_dict(source, '"Loggia","Tak"', 'balcony', details_dict)
            
            added_number += 1

        except NoSuchElementException as exc:
            error = True
            error_no_element += 1
            print(f'Error number: {error_no_element} Offer id: {id}, Error: {exc}')
        
        except TimeoutException as exc:
            error = True
            error_time_out += 1
            print(f'@Error number: {error_time_out} Offer id: {id}, Error:{exc}')

        except WebDriverException as wd_error:
            error_count += 1
            error_web_driver += 1
            print(f'Error number: {error_count} Offer id: {id}, Error: {wd_error}')

        except Exception as exc:
            error = True
            error_another += 1
            error_info = traceback.extract_tb(exc.__traceback__)[-1]  # Get the last element from error stack
            filename = error_info.filename
            line_no = error_info.lineno
            line = error_info.line
            print(f'Error number: {error_another}, Offer id: {id}')
            print(f'Error: {exc}')
            print(f'File: {filename}')
            print(f'Line number: {line_no}')
            print(f'Code line: {line}')
       
        progress_number += 1
        error_count = error_no_element + error_time_out + error_another
        
        if error:
            filename_errors = f'Morizon_links:{datetime.now().strftime("%d%m%Y__%H_%M")}_errors'
            # Save all the links to a CSV file
            with open(f'data/links/{filename_errors}.csv', "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Error link"])
                writer.writerow([offer])

        filename = f'Morizon_data:{datetime.now().strftime("%d%m%Y_%H")}'
        # Save to JSON
        with open(json_file_path, 'a', encoding='utf-8') as jsonfile:
            json.dump(details_dict, jsonfile, ensure_ascii=False, indent=4)
            jsonfile.write(',')
        
        # Save to CSV
        # Check if file exists
        if not os.path.exists(csv_file_path):
            # If file doesn't exist, create it with headers
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=details_dict.keys(), restval="N/A")
                writer.writeheader()

        # Append records to existing file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=details_dict.keys(), restval="N/A")
            writer.writerow(details_dict)

finally:
    driver.quit()
 
end_time = time.time()
execution_time = end_time - start_time

# Print final report
print(f"""Report:
    Execution time: {execution_time} sec
    Added offers: {len(prop_offer_links)}
    Links in base: {added_number}
    effectiveness: {added_number/len(prop_offer_links)*100}%
    empty links: {empty_link}
    errors: {error_count} 
        No element: {error_no_element}
        Time out: {error_time_out}
        Another type: {error_another}
    """)

def get_description(source):
    try:
        # Standard Morizon text that we want to exclude
        morizon_info = "Morizon.pl to serwis w którym znajdziesz"
        
        # Look for description in JSON data
        json_match = re.search(r'"description":"(.*?)"[,}]', source)
        if json_match:
            description = json_match.group(1)
            # Decode JSON escape characters
            description = description.encode().decode('unicode_escape')
            # Check if it's not the standard Morizon text
            if not description.startswith(morizon_info):
                return description
        
        # If not found in JSON, look in other HTML elements
        desc_match = re.search(r'<div[^>]*class="[^"]*description-text[^"]*"[^>]*>(.*?)</div>', source, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            if not description.startswith(morizon_info):
                return description
            
        return None
    except Exception as e:
        print(f"Error extracting description: {e}")
        return None