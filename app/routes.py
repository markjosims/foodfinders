from app import app, db
from flask import Flask, render_template, request, redirect, url_for, jsonify
from app.create_db import Restaurant, City, Cuisine, Locality, City_Table,\
	City_Popular_Cuisine_Junct, City_Popular_Restaurant_Junct, City_Cuisine,\
	Establishment_Cuisine_Junct, Establishment_Locality_Junct
import subprocess
import random
import json


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/restaurants/')
def restaurants():
    places = db.session.query(Restaurant).all()
    return render_template('restaurants.html', places=places)

@app.route('/cuisine/')
def cuisine():
    foods = db.session.query(Cuisine).all()
    return render_template('cuisine.html', foods=foods)

@app.route('/cities/')
def cities():
	"""
	locations = db.session.query(City.name.label('c_name'), City.score)

	nbhds = db.session.query(Locality.name.label('nbhd_name'), Locality.city.label('c_name'))

	place = db.session.query(Restaurant.name.label('r_name'),Restaurant.cuisine.label('r_c_name'),Restaurant.city.label('c_name')).all()

	cities_nbhd = locations.join(nbhds, locations.c_name == nbhds.c_name)
	cities = cities_nbhd.join(place, cities_nbhd.c_name == place.c_name)
	"""
	cities = db.session.query(City).all()

	return render_template('cities.html', cities=cities)

#### You need to hard code all the routes to the NINE instange pages in here ####
@app.route('/restaurant/<val>/')
def restaurant(val):
    restaurant = db.session.query(Restaurant).get(val)
    cuisines = db.session.query(Establishment_Cuisine_Junct.cuisine)\
        .filter(Establishment_Cuisine_Junct.rest_id==val)
    cuisines = [x[0] for x in cuisines] # for some reason the query returns a list of tuples
    if restaurant.address:
    	address = restaurant.address

    addr_split = address.split(" ")	
    addr_format = ""
    for s in addr_split:
    	addr_format = addr_format + "%20" + s

    addr_format = addr_format[2:]
    address = "https://maps.google.com/maps?q=" + addr_format + "&t=&z=13&ie=UTF8&iwloc=&output=embed"
    return render_template('restaurant-instance.html', restaurant=restaurant, cuisines=cuisines, address = address)

@app.route('/city/<val>/')
def city(val):
    city = db.session.query(City).get(val)
    popular_restaurants = db.session.query(City_Popular_Restaurant_Junct)\
        .filter(City_Popular_Restaurant_Junct.city_name==city.name)
    restaurants = [
		db.session.query(Restaurant).get(r.rest_id)\
		for r in popular_restaurants
	]
    popular_cuisine = db.session.query(City_Popular_Cuisine_Junct)\
        .filter(City_Popular_Cuisine_Junct.city_name==city.name)
    localities = db.session.query(Locality)\
        .filter(Locality.city==city.name)
    return render_template('city-instance.html', city=city, restaurants=restaurants,
                           popular_cuisine=popular_cuisine, localities=localities)

@app.route('/cuisinetype/<val>/')
def cuisinetype(val):
    cuisine = db.session.query(Cuisine).get(val)
    places = db.session.query(Establishment_Cuisine_Junct.rest_id)\
        .filter(Establishment_Cuisine_Junct.cuisine==val)
    places = [
		db.session.query(Restaurant).get(place_id[0]) for place_id in places
	]
    cities = db.session.query(City_Cuisine.city_name)\
        .filter(City_Cuisine.cuisine_name==val)
    cities = [x[0] for x in cities] # for some reason the query returns a list of tuples
    
    pop_cities = db.session.query(City_Popular_Cuisine_Junct.city_name)\
        .filter(City_Popular_Cuisine_Junct.cuisine==val)
    pop_cities = [x[0] for x in pop_cities] # for some reason the query returns a list of tuples
    
    # remove popular cities from cities
    cities = [x for x in cities if x not in pop_cities]
    
    return render_template('cuisine-instance.html', cuisine=cuisine, places=places, cities=cities, pop_cities=pop_cities)

@app.route('/test/')
def test():
	p = subprocess.Popen(["coverage", "run", "--branch", "app/tests.py"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.PIPE)
	out, err = p.communicate()
	output=err+out
	output = output.decode("utf-8") #convert from byte type to string type

	q = subprocess.Popen(["coverage", "report", "-m", "--omit", "/env/lib/python3.6/site-packages/*"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.PIPE)
	out, err = q.communicate()
	output2=err+out
	output2 = output2.decode("utf-8")
	# ##############REMOVE IF DON'T WORK############## #
	return render_template('unittest.html', output = output.split("\n"),output2 = output2.split("\n"), len1=len(output), len2=len(output2))

@app.route('/dbtest1/')
def dbtest1():
    restaurant = db.session.query(Restaurant).first()
    #name = restaurant.name
    return render_template('dbtest1.html', restaurant = restaurant)


#### 																		####

@app.route('/sort/')
def sort():
	pass
