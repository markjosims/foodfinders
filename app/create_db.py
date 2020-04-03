import json
from app import db
from app.models import Restaurant, City, Cuisine, Locality, City_Table,\
    City_Popular_Cuisine_Junct, City_Popular_Restaurant_Junct, City_Cuisine,\
    Establishment_Cuisine_Junct, Establishment_Locality_Junct

def load_json(filename):
	with open(filename) as file:
		jsn = json.load(file)
		file.close()

	return jsn
def populate_db():
	zomato_json = load_json('rest_api_info_v2.json')
	restaurant_info = zomato_json['restaurant']
	city_info = zomato_json['city']
	cuisine_info = zomato_json['cuisine']
	#populate the restaurant table
	c_row = 0	#Cuisine junct row
	h_row = 0	#Highlight junct row	
	for r in restaurant_info:
		#Assumed non-nullable info
		rest_id = r['rest_id']
		name = r['name']
		price_per_two = r['price_per_two']
		rating = r['rating']
		#Iterate through cuisines and add to junction table
		rest_cuisines = r['cuisine']
		for c in rest_cuisines:
			e_c_row = Establishment_Cuisine_Junct(row_id = c_row, rest_id = rest_id, cuisine = c)
			db.session.add(e_c_row)
			db.session.commit()
			c_row = c_row + 1
		locality = r['locality']
		city = r['city']

		#Potentially nullable information
		state = r['state']
		address = r['address']
		if r['menu'] != "":
			menu = r['menu']
		else:
			menu = None
		if r['hours'] != "":
			hours = r['hours']
		else:
			hours = None
		if r['coordinates'] != "":
			coordinates = r['coordinates']
		else:
			coordinates = None
		price_rating = r['price']
		if r['thumbnail_url'] != "":
			thumbnail_url = r['thumbnail_url']
		else:
			thumbnail_url = None
		if r['featured_image'] != "":
			featured_image = r['featured_image']
		else:
			featured_image = None
		if r['phone'] != "":
			phone = r['phone']
		else:
			phone = None
		if r['cuisine']:
			cuisine = r['cuisine'][0]
		else:
			cuisine = None
		#Iterate through highlights and add to junction table
		#for h in r['highlights']:
		#	e_h_row = Establishment_Highlights(row_id = h_row, rest_id = rest_id, highlight = h)
		#	db.session.add(e_h_row)
		#	db.session.commit()
		#	h_row = h_row + 1

		new_establishment = Restaurant(name = name, price_per_two = price_per_two, rating = rating, city = city, 
							locality = locality, rest_id = rest_id, state = state, address = address, menu = menu,
							hours = hours, coordinates = coordinates, price_rating = price_rating, 
							thumbnail_url = thumbnail_url, featured_image = featured_image, phone = phone,
       						cuisine=cuisine)

		db.session.add(new_establishment)
		db.session.commit()

	c_row = 0	#City_Cuisine row
	pc_row = 0	#Popular cuisinces row
	pr_row = 0	#Popular restaurant row
	loc_row =0  #Locality row
	city_table_row = 0
	for c in city_info:
		#Assumed non-nullable info
		city_id = c['city_id']
		name = c['name']
		#Fill out locality table
		for n in c['neighborhood']:
			loc_row+=1
			nbhd = Locality(id=loc_row, name = n, city = name)
			db.session.add(nbhd)
			db.session.commit()
		score = c['score']
		#Fill out city_cuisines table
		for cuisine in c['cuisine']:
			cuisine_row = City_Cuisine(row_id = c_row, city_name = name, cuisine_name = cuisine)
			db.session.add(cuisine_row)
			db.session.commit()
			c_row = c_row + 1
   
		#Potentially nullable information
		nightlife_index = c['nightlife_index'] if c['nightlife_index'] else 'N/A'
		num_restaurants = c['num_restaurants'] if c['num_restaurants'] else 'N/A'
		country = c['country'] if c['cuisine'] else 'N/A'
		c_cuisine = c['cuisine'][0] if c['cuisine'] else 'N/A'
		#Fill our popular cuisine junct table
		for cuisine in c['popular_cuisines']:
			pc = City_Popular_Cuisine_Junct(row_id = pc_row, city_name = name, cuisine = cuisine)
			db.session.add(pc)
			db.session.commit()
			pc_row = pc_row + 1
		#Fill out our popular restaurants junct table
		for r in c['popular_restaurants']:
			pr = City_Popular_Restaurant_Junct(row_id = pr_row, rest_id = r, city_name = name)
			db.session.add(pr)
			db.session.commit()
			pr_row = pr_row + 1

		new_city = City(name = name, score = score, nightlife_index = nightlife_index, city_id = city_id,
			num_restaurants = num_restaurants, country = country, cuisine=c_cuisine)
		db.session.add(new_city)
		db.session.commit()

		#Construct the city table info
		est_list = c['establishment'].copy()
		counter = 0
		while len(est_list) != 0 and counter != len(restaurant_info):
			r = restaurant_info[counter]
			if r['rest_id'] in est_list:
				nbhd = r['locality']
				if len(r['cuisine']) != 0:
					cuis = r['cuisine'][0]
				else:
					cuis = ""
				new_row = City_Table(row_id = city_table_row, city_name = name, nbhd = nbhd, establishment = r['name'], cuisine = cuis, score = score)
				city_table_row = city_table_row + 1
				est_list.remove(r['rest_id'])
				db.session.add(new_row)
				db.session.commit()
			counter = counter + 1

	cuisine_table_row = 0
	for c in cuisine_info:
		#Assumed non-nullable info
		name = c['name']
		#Average the price
		l = len(c['price'])
		s = 0
		for p in c['price']:
			s = s + float(p)
		if l == 0:
			avg_price_rating = "N/A"
		else:
			avg_price_rating = str(s/l)
		#Average the rating
		l = len(c['rating'])
		s = 0
		for r in c['rating']:
			s = s + float(r)
		if l == 0:
			avg_rating = "N/A"
		else:
			avg_rating = str(s/l)
		# get id of restaurant
		c_rest_id = c['establishment'][0] if c['establishment'] else "N/A"
		# get name of restaurant
		c_rest = ''
		if c_rest_id == 'N/A':
			c_rest = 'N/A'
		else:
			for r in restaurant_info:
				if r['rest_id'] == c_rest_id:
					c_rest = r['name']
					break
		c_city = ''
		for c in city_info:
			if name in c['cuisine']:
				c_city = c['name']
				break
		new_cuisine = Cuisine(name = name, avg_price_rating = avg_price_rating, avg_rating = avg_rating,
                        rest_id=c_rest_id, rest_name=c_rest, city=c_city)
		db.session.add(new_cuisine)
		db.session.commit()

		"""shouldn't need anymore
		#Fill out cuisine_table info
		for r in restaurant_info:
			for cuis in r['cuisine']:
				if cuis == name:
					new_row = Cuisine_Table(row_id = cuisine_table_row, city = r['city'], nbhd = r['locality'], establishment = r['name'], name = name, avg_rating = avg_rating)
					db.session.add(new_row)
					db.session.commit()
					cuisine_table_row = cuisine_table_row + 1
		"""

"""
def main():
	populate_db()
main()
"""