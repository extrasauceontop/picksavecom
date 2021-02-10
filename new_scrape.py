from sgrequests import SgRequests
from bs4 import BeautifulSoup as bs
from sgzip.dynamic import DynamicZipSearch, SearchableCountries
import json
import pandas as pd

locator_domains = []
page_urls = []
location_names = []
street_addresses = []
citys = []
states = []
zips = []
country_codes = []
store_numbers = []
phones = []
location_types = []
latitudes = []
longitudes = []
hours_of_operations = []

search = DynamicZipSearch(country_codes=[SearchableCountries.USA], max_search_results=100)
store_types = {"Pharmacy": "C",
               "Marketplace": "M",
               "Healthcare Clinic": "LC"}

session = SgRequests()

x = 0
for code in search:

    url = "https://www.picknsave.com/stores/search?searchText=" + code
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    #data = json.loads(bs(session.get(url, headers=headers).text, "html.parser").find_all("script")[-3].text.strip().split("parse(")[1].split("\')")[0][1:].replace("\\", "\\\\").replace("\\\\\\\\\"", ""))

    response = session.get(url, headers=headers).text

    soup = bs(response, "html.parser")
    print(soup)

    data = json.loads(soup.find_all("script")[-3].text.strip().split("parse(")[1].split("\')")[0][1:].replace("\\", "\\\\").replace("\\\\\\\\\"", ""))
    coords = []
    try:
        for item in data["storeSearch"]["storeSearchReducer"]["searchResults"]["fuel"]:

            #print(item)

            locator_domain = "picknsave.com"
            page_url = url
            location_name = item["vanityName"]
            address = item["address"]["addressLine1"]
            city = item["address"]["city"]
            state = item["address"]["stateCode"]
            country = item["address"]["countryCode"]
            zipp = item["address"]["zip"]
            store_number = item["storeNumber"]
            phone = item["phoneNumber"]
            location_type = "fuel"
            latitude = item["latitude"]
            longitude = item["longitude"]
            hour_string = ""
            for day_hours in item["ungroupedFormattedHours"]:
                day = day_hours["displayName"]
                hours = day_hours["displayHours"]

                hour_string = hour_string + day + ": " + hours + ", "

            locator_domains.append(locator_domain)
            page_urls.append(page_url)
            location_names.append(location_name)
            street_addresses.append(address)
            citys.append(city)
            states.append(state)
            country_codes.append(country)
            zips.append(zipp)
            store_numbers.append(store_number)
            location_types.append(location_type)
            latitudes.append(latitude)
            longitudes.append(longitude)
            hours_of_operations.append(hour_string)

            coords.append([latitude, longitude])

    except Exception as ex:
        print("search_number: " + str(x))
        print(code)
        print(data["storeSearch"]["storeSearchReducer"])
        print(ex)

    search.mark_found(coords)
    
    search.mark_found(coords)
    x = x+1
    

df = pd.DataFrame(
    {
        "locator_domain": locator_domains,
        "page_url": page_urls,
        "location_name": location_names,
        "street_address": street_addresses,
        "city": citys,
        "state": states,
        "zip": zips,
        "store_number": store_numbers,
        "phone": phones,
        "latitude": latitudes,
        "longitude": longitudes,
        "hours_of_operation": hours_of_operations,
        "country_code": country_codes,
        "location_type": location_types,
    }
)

df.to_csv(data.csv, index=False)