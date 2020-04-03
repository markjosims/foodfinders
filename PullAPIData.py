import json, requests
import sys
from random import random

def fetchZomatoData(start=0,num_restaurants=20,lat=30.2862175,lon=-97.7415767):
    """Gets API information.
    
    Function which retrieves API information from restaurant and returns
    dict containing basic JSON data.

    Args:
        start: Starting index at which to begin API queries.
        num_restaurants: Number of restaurants to be queried through the search
            API.
        lat: Latitude from -90 to 90 describing origin of search.
        lon: Longitude from -180 to 180 describing origin of search.
    
    Returns:
        JSON-formatted dict containing final index ("start") key, as well as
            keys for city, restaurant, and cuisine data.
    """
    url = "https://developers.zomato.com/api/v2.1/"
    api_key = '387058fcd32522cc34ccc2822f8a5eb4'
    apidata = {}
    num_calls = max(num_restaurants // 20,1)
    #lat = 30.2862175
    #lon = -97.7415767
    #lat = 56.987897
    #lon = -4.933750
    #lat = 70.19895
    #lon = 162.90171

    # get restaurant data
    url_r = url + "search"
    names = []
    data_r = []
    initial_fail = False
    for call_num in range(num_calls):
        fail_calls = 0
        while fail_calls < 2 and initial_fail == False:
            try:
                head_r = {'user-key': api_key}
                params_r = {'lat': str(lat), 'lon': str(lon), 'sort': 'real_distance', 'order': 'asc', 'start': str(call_num*20+start), 'count': '20'}
                r = requests.get(url_r, headers=head_r, params=params_r)
                if __debug__:
                    print("Packet " + str(call_num) + " received with code " + str(r.status_code) + " and size " + str(len(r.json()['restaurants'])))
                data = r.json()
                for val in data['restaurants']:
                    names.append(val['restaurant']['name'])
                    if __debug__:
                        print(val['restaurant']['name'])
                    data_r.append(val)
                break
            except:
                if call_num == 0:
                    initial_fail = True
                fail_calls += 1
                print("Call failed!")

    apidata["restaurant"] = data_r
    if __debug__:
        print(str(len(names)) + " restaurants successfully added from API")
        print(names)

    
    # get city data
    cityIDList = set()
    for restaurant in apidata["restaurant"]:
        id = restaurant["restaurant"]["location"]["city_id"]
        if id not in cityIDList:
            cityIDList.add(id)
    if __debug__:
        print(str(len(cityIDList)) + " city IDs retrieved from restaurant data")
        print(cityIDList)
    
    # snippet from stackoverflow user Ned Batchelder
    lst = list(cityIDList)
    chunkList = [lst[i:i + 20] for i in range(0, len(lst), 20)]

    names = []
    data_c = []
    """
    url_c = url + "cities"
    num_calls = max(len(cityIDList) // 20,1)
    for call_num in range(len(chunkList)):
        cityids = chunkList[call_num]
        citystring = ""
        for id in cityids:
            citystring += str(id) + ","
        print(citystring)
        fail_calls = 0
        while fail_calls < 5:
            try:
                head_c = {'user-key': api_key}
                params_c = {'city_ids': citystring}
                r = requests.get(url_c, headers=head_c, params=params_c)
                print(params_c)
                if __debug__:
                    print("Packet " + str(call_num) + " received with code " + str(r.status_code))
                data = r.json()
                for val in data['location_suggestions']:
                    names.append(val['name'])
                    print(val['name'])
                    data_c.append(val)
                break
            except:
                fail_calls += 1

    if __debug__:
        print("Names of cities added: ")
        print(names)
    apidata["city"] = data_c
    """

    url_c = url + "location_details"
    for id in cityIDList:
        fail_calls = 0
        while fail_calls < 2:
            try:
                head_c = {'user-key': api_key}
                params_c = {'entity_id': id, 'entity_type': 'city'}
                r = requests.get(url_c, headers=head_c, params=params_c)
                print(params_c)
                if __debug__:
                    print("Packet " + str(call_num) + " received with code " + str(r.status_code))
                data = r.json()
                data_c.append(data)
                call_num += 1
                break
            except:
                fail_calls += 1
    apidata["city"] = data_c
    if __debug__:
        print(str(len(data_c)) + " cities successfully added from API")
        for val in data_c:
            #print(val['city'])
            pass


    """
    # get cuisine data
    url_r = url + "search"
    head_r = {'user-key': api_key}
    r = requests.get(url_r, headers=head_r)
    if __debug__:
        print("Packet received with code " + str(r.status_code))
    apidata["cuisine"] = r.json()
    """


    return apidata

def parseData(apidata):
    """Parses API data into model format.
    
    Function which parses data retrieved from API via fetchZomatoData into a
        format which is more similar to final model structure.

    Args:
        apidata: Pointer to api-data dict.
    
    Returns:
        Pointer to parsed dict.
    """

    # parses API data and translates it into JSON in database format
    model_data = {}
    rest_list = apidata['restaurant']
    city_list = apidata['city']
    cuisine_list = set()
    
    # iterate through each city and update model
    model_data['city'] = []
    for c in city_list:
        entry = {}
        entry['city_id'] = str(c['location']['city_id'])
        entry['name'] = c['location']['city_name']
        entry['neighborhood'] = []
        entry['score'] = str(c['popularity'])
        entry['nightlife_index'] = c['nightlife_index']
        # below two entries are added later
        entry['establishment'] = []
        entry['cuisine'] = []
        entry['num_restaurants'] = str(c['num_restaurant'])
        entry['country'] = c['location']['country_name']
        try:
            entry['popular_cuisines'] = c['top_cuisines']
        except:
            entry['popular_cuisines'] = []
        for cuisine in entry['popular_cuisines']:
            if cuisine not in cuisine_list:
                cuisine_list.add(cuisine)

        top_restaurant_ids = []
        for rest in c['best_rated_restaurant']:
            top_restaurant_ids.append(str(rest['restaurant']['R']['res_id']))
        entry['popular_restaurants'] = top_restaurant_ids
        rest_list.extend(c['best_rated_restaurant'])
        model_data['city'].append(entry)

    # iterate through each restaurant and update model
    model_data['restaurant'] = []
    idlist = set()
    for r in rest_list:
        entry = {}
        rest = r['restaurant']
        if rest['id'] in idlist:
            continue
        else:
            idlist.add(rest['id'])
        entry['rest_id'] = str(rest['id'])
        entry['name'] = rest['name']
        entry['price'] = str(rest['price_range'])
        entry['rating'] = str(rest['user_rating']['aggregate_rating'])
        entry['cuisine'] = list(filter(None,rest['cuisines'].split(', ')))
        entry['locality'] = rest['location']['locality']
        for cuisine in entry['cuisine']:
            if cuisine not in cuisine_list:
                cuisine_list.add(cuisine)
        entry['city_id'] = str(rest['location']['city_id'])
        for city in model_data['city']:
            if city['city_id'] == entry['city_id']:
                city['establishment'].append(str(entry['rest_id']))
                if entry['locality'] not in city['neighborhood']:
                    city['neighborhood'].append(entry['locality'])
                city['cuisine'] = list(set(city['cuisine']).union(set(entry['cuisine'])))
        entry['city'] = rest['location']['city']
        # FIX STATE CALL LATER
        entry['state'] = 'Texas'
        entry['address'] = rest['location']['address']
        # menu is technically in the API but would require too many calls
        entry['menu'] = rest['menu_url']
        entry['hours'] = rest['timings']
        entry['coordinates'] = rest['location']['latitude'] + ',' + rest['location']['longitude']
        entry['price_per_two'] = str(rest['average_cost_for_two'])
        entry['thumbnail_url'] = rest['thumb']
        entry['featured_image'] = rest['featured_image']
        entry['phone'] = rest['phone_numbers']
        entry['highlights'] = rest['highlights']
        model_data['restaurant'].append(entry)
    
    # iterate through each cuisine and update model
    model_data['cuisine'] = []
    for cuisine in cuisine_list:
        entry = {}
        entry['name'] = cuisine
        cities = set()
        for city in model_data['city']:
            if cuisine in city['popular_cuisines']:
                cities.add(city['city_id'])
        entry['top_city'] = list(cities)
        restaurants = set()
        prices = set()
        ratings = set()
        for rest in model_data['restaurant']:
            if cuisine in rest['cuisine']:
                restaurants.add(rest['rest_id'])
                prices.add(rest['price'])
                ratings.add(rest['rating'])
        entry['price'] = list(prices)
        entry['rating'] = list(ratings)
        entry['establishment'] = list(restaurants)
        entry['typical_foods'] = None
        model_data['cuisine'].append(entry)

    return model_data   


#def checkIntegrityOfDBData(dbdata):
    # verifies that non-nullable with missing values is removed
    #return

def mergeDataFiles(old_dat,new_dat):
    """Function which updates old_dat with new_dat information.

    Args:
        old_dat: Pointer to api-data dict containing priority information.
        new_dat: Pointer to api-data dict containing new information.
    
    Returns:
        Pointer to updated dict.
    """
    # merges two json files
    if __debug__:
        print("Merging old json (" + str(len(old_dat['restaurant'])) + " restaurants, " +
              str(len(old_dat['city'])) + " cities, " + str(len(old_dat['cuisine'])) +
              " cuisines) with new json (" + str(len(new_dat['restaurant'])) + " restaurants, " +
              str(len(new_dat['city'])) + " cities, " + str(len(new_dat['cuisine'])) +
              " cuisines)")

    # merge cities
    old_city = old_dat['city']
    new_city = new_dat['city']
    old_ids = set()
    for city in old_city:
        old_ids.add(city['city_id'])
    for city in new_city:
        if city['city_id'] not in old_ids:
            old_city.append(city)
    if __debug__:
        print("Finished merging cities (patch still needed)!")
    
    # merge restaurants
    old_rest = old_dat['restaurant']
    new_rest = new_dat['restaurant']
    old_ids = set()
    for rest in old_rest:
        old_ids.add(rest['rest_id'])
    for rest in new_rest:
        if rest['rest_id'] not in old_ids:
            old_rest.append(rest)
            for city in old_dat['city']:
                if city['city_id'] == rest['city_id']:
                    city['establishment'].append(str(rest['rest_id']))
                    if rest['locality'] not in city['neighborhood']:
                        city['neighborhood'].append(rest['locality'])
                    city['cuisine'] = list(set(city['cuisine']).union(set(rest['cuisine'])))

    if __debug__:
        print("Finished merging restaurants and patching cities!")
    
    # merge cuisines
    old_cuisine = old_dat['cuisine']
    new_cuisine = new_dat['cuisine']
    old_ids = set()
    for cuisine in old_cuisine:
        old_ids.add(cuisine['name'])
    for cuisine in new_cuisine:
        if cuisine['name'] not in old_ids:
            old_cuisine.append(cuisine)
    
    if __debug__:
        print("Finished merging cuisines!")
        print("Final json contains " + str(len(old_dat['restaurant'])) +
              " restaurants, " + str(len(old_dat['city'])) + " cities, " +
              str(len(old_dat['cuisine'])) + " cuisines")
    
    return old_dat 


def retrieveData(filepath,num_restaurants=120,update=False,lat=30.2862175,
                 lon=-97.7415767):
    """Gets data from API and saves it to file.
    
    Master function which organizes api retrieval and storage operations.
        Uses temp file old_data.json to store data in case of interruption
        during write operations (corruption of data).

    Args:
        filepath: Filepath of json to be updated/json to be saved.
        num_restaurants: Number of restaurants to be queried in initial calls.
        update: Flags if json should be updated or rewritten.
        lat: Latitude from -90 to 90 describing origin of search.
        lon: Longitude from -180 to 180 describing origin of search.
    
    Returns:
        Pointer to parsed dict.
    """
    # master function which retrieves JSON information and stores it in
    # filepath as a modified JSON for database use
    start = 0
    if update:
        with open(filepath,'r') as old_json_file:
            old_dat = json.loads(old_json_file.read())
            with open('old_data.json','w') as backup:
                json.dump(old_dat,backup,indent=4)
        if 'start' in old_dat.keys():
            #start = int(old_dat['start'])
            pass
    apidata = fetchZomatoData(start=start,num_restaurants=num_restaurants,
                              lat=lat,lon=lon)
    apidata = parseData(apidata)
    if update:
        apidata = mergeDataFiles(old_dat,apidata)
    apidata['start'] = start + num_restaurants
    #checkIntegrityOfAPIData(apidata)
    with open(filepath,'w') as new_json_file:
        json.dump(apidata, new_json_file, indent=4)
    if __debug__:
        print("JSON successfully written to file!\nAPI data pull complete\n\n")
    return

def main():
    """Main method.  Not meant to be used in modular operation.  Currently
        used to coordinate a random search functionality with retrieveData.
    """
    #retrieveData("./rest_api_info.json",update=False)
    for i in range(50):
        lat = float(random()*359-179.5)
        lon = float(random()*179-89.5)
        print("starting iteration " + str(i) + " with coordinates " +
              str(lat) + ", " + str(lon))
        retrieveData("./rest_api_info_v2.json",lat=lat,lon=lon,update=True)

if __name__ == '__main__':
    main()