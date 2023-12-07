#regex
variable_html = r'<[^<]+?>'
variable_white = r'\s+'
platform = r'https://www\.([^/]+)\.pl/oferta/'
link_content = r'/oferta/(.*?)$'
property_levels = r'"Piętro","(\d+/\d+)"'
description_p = r'<p>(.*?)</p>'
description_d = r'<div>(.*?)</div>'
market_type = r'\\"rynek\\":\\"([aA-zZ]*)\\",'
building_type = r'"Typ budynku","([aA-zZ]*)",'
no_rooms = r'\\"number_of_rooms\\":([1-9]*),\\'
kitchen_type = r'"Typ kuchni","([aA-zZ]*)",'
building_year = r'"Rok budowy","(\d+)",'
material = r'"Materiał budowlany","([^"]*)",'
heating_type = r'"Ogrzewanie","([^"]*)",'
water = r'"water","([^"]*)",'


