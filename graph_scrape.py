import os
from sgrequests import SgRequests
from sgzip.dynamic import DynamicZipSearch, SearchableCountries
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

headers = {'User-Agent': 'PostmanRuntime/7.19.0', "Upgrade-Insecure-Requests": "1", "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
session = SgRequests(retry_behavior=None)
url = 'https://www.picknsave.com/stores/api/graphql'
search = DynamicZipSearch(country_codes=[SearchableCountries.USA])

for postal in search:
    data = {
        "query": "\n      query storeSearch($searchText: String!, $filters: [String]!) {\n        storeSearch(searchText: $searchText, filters: $filters) {\n          stores {\n            ...storeSearchResult\n          }\n          fuel {\n            ...storeSearchResult\n          }\n          shouldShowFuelMessage\n        }\n      }\n      \n  fragment storeSearchResult on Store {\n    banner\n    vanityName\n    divisionNumber\n    storeNumber\n    phoneNumber\n    showWeeklyAd\n    showShopThisStoreAndPreferredStoreButtons\n    storeType\n    distance\n    latitude\n    longitude\n    tz\n    ungroupedFormattedHours {\n      displayName\n      displayHours\n      isToday\n    }\n    address {\n      addressLine1\n      addressLine2\n      city\n      countryCode\n      stateCode\n      zip\n    }\n    pharmacy {\n      phoneNumber\n    }\n    departments {\n      code\n    }\n    fulfillmentMethods{\n      hasPickup\n      hasDelivery\n    }\n  }\n",
        "variables": {
            "searchText": postal,
            "filters": []
        },
        "operationName": "storeSearch"
    }
    response = session.post(url, json=data, headers=headers).json()
    print(response)
    x = 0
    coords = []
    if x % 100 == 0:
        session = ""
        session = SgRequests()
    try:
        for item in data["data"]["storeSearch"]["storeSearchReducer"]["searchResults"]["fuel"]:

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

            print(x)
            print(location_name)
            print("")

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
        print(postal)
        print(data["storeSearch"]["storeSearchReducer"])
        print(ex)

    
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
