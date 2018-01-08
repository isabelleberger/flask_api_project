from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import geocoder
import urllib
import json
import geopy.distance

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash, password)

# b = Bus()
# buses = b.query("500 H Street NE Washington DC")
class Bus(object):
	def address_to_latlng(self, address):
		g = geocoder.google(address)
		return (g.lat, g.lng)
        def latlng_to_dist(self, lat1, lng1, lat2, lng2):
                dist = geopy.distance.vincenty((lat1,lng1),(lat2,lng2)).miles
                return dist
	def query(self, address):
		lat1, lng1 = self.address_to_latlng(address)
		print(lat1, lng1)

		query_url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/53/query?where=1%3D1&outFields=LATITUDE,LONGITUDE,BSTP_MSG_TEXT,BSTP_IFC_OWN&outSR=4326&f=json"
		g = urllib.request.urlopen(query_url)
		results = g.read()
		g.close()

		data = json.loads(results)
		print(data)
		buses=[]
		for bus in data['features']:
		    stop_name = bus['attributes']['BSTP_MSG_TEXT']
		    lat2 = bus['attributes']['LATITUDE']
		    lng2 = bus['attributes']['LONGITUDE']
		    dist = self.latlng_to_dist(lat1, lng1, lat2, lng2)
                    own = bus['attributes']['BSTP_IFC_OWN']
                    #only query buses less than a mile from search location
                    if dist < 1:    
		        d = {
			    'name': stop_name,
			    'own': own,
			    'lat': lat2,
			    'lng': lng2,
                            'dist': dist
		        }
		        buses.append(d)
                closest = min(buses, key=lambda x:x['dist'])
		return buses, closest

# p = Place()
# places = p.query("1600 Ampitheater Parkway Mountain View CA")
class Place(object):
	def meters_to_walking_time(self, meters):
		# 80 meters is one minute walking time
		return int(meters / 80)
	def wiki_path(self, slug):
		return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(" ","_"))
	def address_to_latlng(self, address):
		g = geocoder.google(address)
		return (g.lat, g.lng)
	def query(self, address):
		lat, lng = self.address_to_latlng(address)
		print(lat, lng)

		query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat,lng)
		g = urllib.request.urlopen(query_url)
		results = g.read()
		g.close()

		data = json.loads(results)
		print(data)

		places = []
		for place in data['query']['geosearch']:
			name = place['title']
			meters = place['dist']
			lat = place['lat']
			lng = place['lon']

			wiki_url = self.wiki_path(name)
			walking_time = self.meters_to_walking_time(meters)

			d = {
				'name': name,
				'url': wiki_url,
				'time': walking_time,
				'lat': lat,
				'lng': lng  
			}

			places.append(d)
		return places

