from app import db

###				Model Classes				###
class Restaurant(db.Model):
	__tablename__='restaurant'

	#Non-nullable table information
	name = db.Column(db.String(), nullable = False)
	price_per_two = db.Column(db.String(), nullable = False)
	rating = db.Column(db.String(), nullable = False)
	city = db.Column(db.String(),  nullable = False)
	locality = db.Column(db.String(),  nullable = False)

	rest_id = db.Column(db.String(), primary_key = True)

	#Optional instance page information
	cuisine = db.Column(db.String(), nullable = True)
	state = db.Column(db.String(), nullable = True)
	address = db.Column(db.String(), nullable = True)
	menu = db.Column(db.String(), nullable = True)				#URL
	hours = db.Column(db.String(), nullable = True)
	coordinates = db.Column(db.String(), nullable = True)		#It looks like "x, y"
	price_rating = db.Column(db.String(), nullable = True)	#I'm guessing this is a 1-5 rating
	thumbnail_url = db.Column(db.String(), nullable = True)		#URL
	featured_image = db.Column(db.String(), nullable = True)	#URL For Zomato
	phone = db.Column(db.String(), nullable = True)

class City(db.Model):
	__tablename__ = 'city'

	#Non-nullable table information
	name = db.Column(db.String(), primary_key = True)
	score = db.Column(db.String(), nullable = False)
	nightlife_index = db.Column(db.String(), nullable = False)
	num_restaurants = db.Column(db.String(), nullable = False)
	country = db.Column(db.String(), nullable = False)
	cuisine = db.Column(db.String(), nullable = False)

	#Optional instance page information
	city_id = db.Column(db.String(), nullable = True) 
class City_Table(db.Model):
	__tablename__ = 'city_table'
	row_id = db.Column(db.String(), primary_key = True)
	city_name = db.Column(db.String(), nullable = False)
	nbhd = db.Column(db.String(), nullable = False)
	establishment = db.Column(db.String(), nullable = False)
	cuisine = db.Column(db.String(), nullable = False)
	score = db.Column(db.String(), nullable = False)

class Cuisine(db.Model):
	__tablename__ = 'cuisine'
	
	#Non-nullable table information
	name = db.Column(db.String(), primary_key = True) 		#For the time being, assume this is one word
	avg_price_rating = db.Column(db.String(), nullable = False)	#Avg the ratings
	avg_rating = db.Column(db.String(), nullable = False)			#Averag the ratings
	rest_id = db.Column(db.String(), nullable = False)
	rest_name = db.Column(db.String(), nullable = False)
	city = db.Column(db.String(), nullable = False)

class Locality(db.Model):
	__tablename__ = 'locality'

	#Non-nullable information
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable = False)
	city = db.Column(db.String(), nullable = False)


###				Junction Classes				###

### City Junctions
class City_Popular_Cuisine_Junct(db.Model):
	__tablename__ = 'city_popular_cuisine_junct'

	row_id = db.Column(db.Integer, primary_key = True)
	city_name = db.Column(db.String(80), nullable = False)
	cuisine = db.Column(db.String(80), nullable = False)

class City_Popular_Restaurant_Junct(db.Model):
	__tablename__ = 'city_popular_restaurant_junct'

	row_id = db.Column(db.Integer, primary_key = True)
	rest_id = db.Column(db.String(80), nullable = False)
	city_name = db.Column(db.String(80), nullable = False)	

class City_Cuisine(db.Model):
	__tablename__ = 'city_cuisine'

	row_id = db.Column(db.Integer, primary_key = True)
	city_name = db.Column(db.String(80), nullable = False)
	cuisine_name = db.Column(db.String(80), nullable = False)

### Establishment/Cuisine Junctions
class Establishment_Cuisine_Junct(db.Model):
	__tablename__ = 'establishment_cuisine_junct'

	row_id = db.Column(db.Integer, primary_key = True)
	rest_id = db.Column(db.String(80), nullable = False)
	cuisine = db.Column(db.String(80), nullable = False)

### Establishment Junctions
class Establishment_Locality_Junct(db.Model):
	__tablename__ = 'establishment_locality_junct'

	row_id = db.Column(db.Integer, primary_key = True)
	rest_id = db.Column(db.String(80), nullable = False)
	cuisine = db.Column(db.String(80), nullable = False)						### FIX THIS ###

"""
class Establishment_Highlights(db.Model):
	__tablename__ = 'establishment_highlights'

	row_id = db.Column(db.Integer, primary_key = True)
	rest_id = db.Column(db.String(80), nullable = False)	
	highlight = db.Column(db.String(80), nullable = False)
"""

def make_db():
	db.drop_all()
	db.create_all()
