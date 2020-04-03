import os
import sys
import unittest
from models import db, Restaurant, City, Cuisine, Locality, City_Popular_Cuisine_Junct, City_Popular_Restaurant_Junct, City_Cuisine, Establishment_Cuisine_Junct, Establishment_Locality_Junct

###         Unittests                  ###
class Tests(unittest.TestCase):

    def testRestaurantDB(self):

        # Put in example information
        s = Restaurant(name = 'Boring Name', price_per_two = '10000', rating = '0.0', city = 'North Pole', locality = 'Bad Neighborhood', rest_id = '10000')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(Restaurant).filter_by(name = 'Boring Name').one()
        self.assertEqual(str(r.name), 'Boring Name')
        self.assertEqual(str(r.price_per_two), '10000')
        self.assertEqual(str(r.rating), '0.0')
        self.assertEqual(str(r.city), 'North Pole')
        self.assertEqual(str(r.locality), 'Bad Neighborhood')
        self.assertEqual(str(r.rest_id), '10000')

        # Delete example information once done
        db.session.query(Restaurant).filter_by(name = 'Boring Name').delete()
        db.session.commit()

    def testCityDB(self):

        # Put in example information
        s = City(name = 'Boring Name', score = '0.1', num_restaurants = '0', country = 'Mars', nightlife_index = '5.0', cuisine='Food')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(City).filter_by(name = 'Boring Name').one()
        self.assertEqual(str(r.name), 'Boring Name')
        self.assertEqual(str(r.score), '0.1')
        self.assertEqual(str(r.num_restaurants), '0')
        self.assertEqual(str(r.country), 'Mars')
        self.assertEqual(str(r.nightlife_index), '5.0')
        self.assertEqual(str(r.cuisine), 'Food')

        # Delete example information once done
        db.session.query(City).filter_by(name = 'Boring Name').delete()
        db.session.commit()


    def testCuisineDB(self):

        # Put in example information
        s = Cuisine(name = 'Boring Name', avg_price_rating = '0.2', avg_rating = '0', rest_id='1337', rest_name='FoodShack', city='Cidade')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(Cuisine).filter_by(name = 'Boring Name').one()
        self.assertEqual(str(r.name), 'Boring Name')
        self.assertEqual(str(r.avg_price_rating), '0.2')
        self.assertEqual(str(r.avg_rating), '0')
        self.assertEqual(str(r.rest_id), '1337')
        self.assertEqual(str(r.rest_name), 'FoodShack')
        self.assertEqual(str(r.city), 'Cidade')

        # Delete example information once done
        db.session.query(Cuisine).filter_by(name = 'Boring Name').delete()
        db.session.commit()

    
    def testLocalityDB(self):

        # Put in example information
        s = Locality(id=9999, name = 'Boring Name', city = 'Atlantis')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(Locality).filter_by(name = 'Boring Name').one()
        self.assertEqual(r.id, 9999)
        self.assertEqual(str(r.name), 'Boring Name')
        self.assertEqual(str(r.city), 'Atlantis')

        # Delete example information once done
        db.session.query(Locality).filter_by(name = 'Boring Name').delete()
        db.session.commit()
    
    def testCityPopularCuisineJunctDB(self):

        # Put in example information
        s = City_Popular_Cuisine_Junct(row_id = '10000', city_name = 'Atlantis', cuisine = 'Trash')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(City_Popular_Cuisine_Junct).filter_by(row_id = '10000').one()
        self.assertEqual(str(r.row_id), '10000')
        self.assertEqual(str(r.city_name), 'Atlantis')
        self.assertEqual(str(r.cuisine), 'Trash')

        # Delete example information once done
        db.session.query(City_Popular_Cuisine_Junct).filter_by(row_id = '10000').delete()
        db.session.commit()

    def testCityPopularRestaurantJunctDB(self):

        # Put in example information
        s = City_Popular_Restaurant_Junct(row_id = '10000', rest_id = '10000', city_name = 'Atlantis')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(City_Popular_Restaurant_Junct).filter_by(row_id = '10000').one()
        self.assertEqual(str(r.row_id), '10000')
        self.assertEqual(str(r.rest_id), '10000')
        self.assertEqual(str(r.city_name), 'Atlantis')

        # Delete example information once done
        db.session.query(City_Popular_Restaurant_Junct).filter_by(row_id = '10000').delete()
        db.session.commit()

    def testCityCuisineDB(self):

        # Put in example information
        s = City_Cuisine(row_id = '10000', city_name = 'Atlantis', cuisine_name = 'Trash')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(City_Cuisine).filter_by(row_id = '10000').one()
        self.assertEqual(str(r.row_id), '10000')
        self.assertEqual(str(r.city_name), 'Atlantis')
        self.assertEqual(str(r.cuisine_name), 'Trash')

        # Delete example information once done
        db.session.query(City_Cuisine).filter_by(row_id = '10000').delete()
        db.session.commit()

    def testEstablishmentCuisineJunctDB(self):

        # Put in example information
        s = Establishment_Cuisine_Junct(row_id = '10000', rest_id = '10000', cuisine = 'Trash')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(Establishment_Cuisine_Junct).filter_by(row_id = '10000').one()
        self.assertEqual(str(r.row_id), '10000')
        self.assertEqual(str(r.rest_id), '10000')
        self.assertEqual(str(r.cuisine), 'Trash')

        # Delete example information once done
        db.session.query(Establishment_Cuisine_Junct).filter_by(row_id = '10000').delete()
        db.session.commit()

    def testEstablishmentLocalityJunctDB(self):

        # Put in example information
        s = Establishment_Locality_Junct(row_id = '10000', rest_id = '10000', cuisine = 'Trash')
        db.session.add(s)
        db.session.commit()

        # Check for expected example information
        r = db.session.query(Establishment_Locality_Junct).filter_by(row_id = '10000').one()
        self.assertEqual(str(r.row_id), '10000')
        self.assertEqual(str(r.rest_id), '10000')
        self.assertEqual(str(r.cuisine), 'Trash')

        # Delete example information once done
        db.session.query(Establishment_Locality_Junct).filter_by(row_id = '10000').delete()
        db.session.commit()
    

if __name__ == "__main__":
    unittest.main()
