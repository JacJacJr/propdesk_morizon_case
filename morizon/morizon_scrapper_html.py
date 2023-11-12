import re
import csv
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import regex_list as reg
    
def save_to_dict(details_dict, key, variable):
    if variable is not None and variable != '' and variable != []:
        if type(variable) is int or type(variable) is str:
            #change coma for other separator
            #TODO change all regex as variable from regex_list
            variable = str(variable).replace(',', ' ')
            variable = re.sub('<[^<]+?>', '', variable)
            details_dict[key] = variable    
        elif type(variable) is list:
            variable = ' '.join(variable)
            variable = variable.replace(',', ' ')
            variable = re.sub('<[^<]+?>', '', variable)
            variable = re.sub('\s+', ' ', variable).strip()
            details_dict[key] = variable  
        else: 
            details_dict[key] = 'n/a'
            print(f'Other type of viriable in save_to_dict in {key}')
    else:
        variable = 'NULL'
        details_dict[key] = variable

prop_offer_links = pd.read_csv('data/test.csv')

options = Options()
options.add_argument('--headless') 
driver = webdriver.Firefox(options=options)

error_number = 0
added_number = 0
empty_link = 0 
try:
    for offer in prop_offer_links.iloc[:, 0]:
        try:
            driver.get(offer)

            #save whole html for processing
            source = driver.page_source

            phrases_to_check = ["którego szukasz, jest już nieaktualne", "Brak ofert spełniających Twoje kryteria", "Pod tym adresem nic nie ma...", "https://www.morizon.pl/_nuxt/error404.e3aeda20.svg"]
            if any(phrase in source for phrase in phrases_to_check):
                empty_link += 1
                continue 
            else:
                details_dict = {}       

                save_to_dict(details_dict, 'url', offer)     

                #informations from url 
                platform = re.findall(r'https://www\.([^/]+)\.pl/oferta/', offer)
                save_to_dict(details_dict, 'platform', platform)

                link_content = re.findall(r'/oferta/(.*?)$', offer)

                link_content = link_content[0] 
                link_parts = link_content.split('-')
                
                transaction_type  = link_parts.pop(0)
                save_to_dict(details_dict, 'transaction_type', transaction_type)  

                property_type = link_parts.pop(0)
                save_to_dict(details_dict, 'property_type',property_type)            

                city = link_parts.pop(0)
                save_to_dict(details_dict, 'city', city)

                id = link_parts.pop(-1)
                save_to_dict(details_dict, 'id', id)  

                total_area = link_parts.pop(-1)[:-2]
                save_to_dict(details_dict,'total_area', total_area)

                if len(link_parts) > 0:
                    district = link_parts.pop(0)
                    two_word_district = ['polnoc', 'północ', 'południe', 'poludnie']

                    if any(word in link_parts[0] for word in two_word_district):
                        district = district + ' ' + link_parts.pop(0)

                    if len(link_parts) <= 0:
                        prec_adress = 'n/a'
                    else:
                        prec_adress = ' '.join(link_parts)
                else:
                    district = 'n/a'
                    
                save_to_dict(details_dict,'district', district)
                save_to_dict(details_dict,'prec_adress', prec_adress)

                #informations from html source
                #prices
                prices = driver.find_element(By.CSS_SELECTOR, "#basic-info-price-row > div").text
                if prices in ['ZAPYTAJ O CENĘ']:
                    row_price = "n/a"
                    row_price_m2 = "n/a"
                    primary_market = 1
                else:
                    row_price = prices.split("zł")[0].strip()
                    row_price_m2 = prices.split("zł")[1].strip()
                    primary_market = "n/a"
                
                save_to_dict(details_dict,'row_price', row_price)
                save_to_dict(details_dict,'row_price_m2', row_price_m2)
                save_to_dict(details_dict,'primery_market', row_price)
                
                #floors
                property_levels = re.findall(r'"Piętro","(\d+/\d+)"', source)

                if property_levels:
                    try:
                        property_level, total_property_level = property_levels[0].split('/')
                    except ValueError:
                        print(f'No informations about property_levels in {id}')
                else:
                    property_level = 'n/a'
                    total_property_level = 'n/a'

                save_to_dict(details_dict,'property_level', property_level)
                save_to_dict(details_dict,'total_property_level', total_property_level)

                #regex without split functions
                description = re.findall(r'<p>(.*?)</p>', source, re.DOTALL)
                if description == []:
                    description = re.findall(r'<div>(.*?)</div>', source, re.DOTALL)
                    print('to ten')
                    print(offer)
                    print(description)
                save_to_dict(details_dict,'description', description)

                market_type = re.findall(r'\\"rynek\\":\\"([aA-zZ]*)\\",', source)
                save_to_dict(details_dict,'market_type', market_type)

                building_type = re.findall(r'"Typ budynku","([aA-zZ]*)",', source)
                save_to_dict(details_dict,'building_type', building_type)

                no_rooms = re.findall(r'\\"number_of_rooms\\":([1-9]*),\\', source)
                save_to_dict(details_dict,'no_rooms', no_rooms)

                kitchen_type = re.findall(r'"Typ kuchni","([aA-zZ]*)",', source)
                save_to_dict(details_dict,'kitchen_type', kitchen_type)

                building_year = re.findall(r'"Rok budowy","(\d+)",', source)
                save_to_dict(details_dict,'building_year', building_year)

                material = re.findall(r'"Materiał budowlany","([^"]*)",', source)
                save_to_dict(details_dict,'material', material)

                heating_type = re.findall(r'"Ogrzewanie","([^"]*)",', source)
                save_to_dict(details_dict,'heating_type', heating_type)

                water = re.findall(r'"water","([^"]*)",', source)
                save_to_dict(details_dict,'water', water)

                #conditions on html source (encoded)
                if ',"Winda",' in source:
                    elevator = 1
                else:
                    elevator = 0
                save_to_dict(details_dict,'elevator', elevator)

                if ',"Gaz",' in source:
                    gas = 1
                else:
                    gas = 0
                save_to_dict(details_dict,'gas', gas)

                if '"Balkon","Tak"' or '"Loggia","Tak"' in source :
                    balcony = 1
                else:
                    balcony = 0
                save_to_dict(details_dict,'balcony', balcony)

                if '"Łazienka razem z WC","Tak"' in source:
                    bath_with_wc = 1
                else:
                    bath_with_wc = 0
                save_to_dict(details_dict, 'bath_with_wc', bath_with_wc)

                if '="Prąd"' in source:
                    electricity = 1
                else:
                    electricity = 0
                save_to_dict(details_dict,'electricity', electricity)

                if 'parking_places' in source:
                    parking = 1
                else:
                    parking = 0
                save_to_dict(details_dict,'parking', parking)

                if '>Piwnica<' in source:
                    basement = 1
                else:
                    basement = 0
                save_to_dict(details_dict,'basement', basement)
                
                added_number += 1
                print(f'Progress: {added_number}/{len(prop_offer_links)}\n {offer}')

        except NoSuchElementException as no_element:
            error_number += 1
            print(f'Error number: {error_number} Offer id: {id}, Error: {no_element}')

        except Exception as exc:
            error_number += 1
            print(f'@@@ Error number: {error_number} Offer id: {id}, Error:{exc}')
        
        filename = f'Morizon_data:{datetime.now().strftime("%d%m%Y_%H")}'
        #save to json
        with open(f'{filename}.json', 'a', encoding='utf-8') as jsonfile:
            json.dump(details_dict, jsonfile, indent=4)
            jsonfile.write(',')
        #save to csv
        all_keys = [d for d in details_dict.keys()]

        with open(f'{filename}.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=all_keys, restval="N/A")
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(details_dict)
    
finally:
    driver.quit()
 
print(f"""Raport:
    Added offers: {len(prop_offer_links)}
    Links in base: {added_number}
    effectiveness: {added_number/len(prop_offer_links)*100}%
    errors: {error_number}
    empty links: {empty_link}
    """)