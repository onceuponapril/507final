
from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import json
import urllib
from urllib.parse import urlencode
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient

map_api='AIzaSyCDFrR1bowszXuQLUG8f3pj61Q_Uc_mnzA'
# 1.cache
CACHE_FNAME = 'checkcache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url,params=None):
    if params!=None:
       qstr=urlencode(params)
       nurl=url+"?"+qstr
       return nurl
    else:
        return url

def make_request_using_cache(url,params=None):
    unique_ident = get_unique_key(url,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")


        resp = requests.get(url,params)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

# 2 WRITE INTO DB


DBNAME='Foddie_Map.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
#
# statement = '''
#     DROP TABLE IF EXISTS 'EAT';
# '''
# cur.execute(statement)
#
statement = '''
    DROP TABLE IF EXISTS 'RIDE';
'''
cur.execute(statement)

# statement='''CREATE TABLE EAT(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'Name' TEXT NOT NULL,
# 'Phone' TEXT,
# 'Price' TEXT,
# 'Rating ' NUMERIC,
# 'address' TEXT,
# 'lag_log' TEXT
# )'''
# cur.execute(statement)
# conn.commit()

statement='''CREATE TABLE RIDE(
'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
'Start' TEXT NOT NULL,
'Desitination' TEXT NOT NULL,
'Estimated time (minute)' TEXT,
'Estimated distance(miles)' TEXT,
'Estimated maximun cost (dollar)' TEXT,
'Estimated minimum cost (dollar)' TEXT)
'''
cur.execute(statement)
conn.commit()

# 3.1 google maps
class google_map():
    def __init__(self,address):
        self.addr=address

    def lat_log(address):

        map_url='https://maps.googleapis.com/maps/api/place/textsearch/json'
        params={}
        params['key']=map_api
        params['query']=str(address)
        req=make_request_using_cache(map_url,params=params)
        rstxt=json.loads(req)
        rs=rstxt['results']
        geoloc=rs[0]['geometry']['location']

        lat=geoloc['lat']
        log=geoloc['lng']
        loc="{},{}".format(lat,log)

        return loc
        #
        # #2

    # def nearby(address):

#make_request_using_cache
#
#     def image():
#         https://developers.google.com/places/web-service/details
#     def "international_phone_number"
#     def type
#     def ratings
#     def time


# 3. yelp data
# user_input='San Francisco'
# baseurl="https://www.yelp.com/"
# search_url=baseurl+'search'
# param={}
# param['find_desc']="Top+100+Places+to+Eat"
# param['find_loc']=user_input
# n=range(20)
#
# count=0
# while count<100:
#     for i in n:
#         param['start']=i*10
#         html=make_request_using_cache(search_url,param)
#         soup_a = BeautifulSoup(html, 'html.parser')
#         list_of_eat=soup_a.find_all("li",class_="regular-search-result")
#
#         for eat in list_of_eat:
#             try:
#                 name=eat.find('a',class_='biz-name').text.strip()
#                 phone=eat.find('span',class_='biz-phone').text.strip()
#                 price=eat.find('span',class_="business-attribute price-range").text.strip()
#                 rating=eat.find('div',class_='i-stars')['title'][:3]
#                 add=eat.find('address').text.strip()
#                 lat_log=google_map.lat_log(add)
#                 count+=1
#
#                 params=(name,phone,price,rating,add,lat_log)
#                 statement='''INSERT INTO EAT VALUES(Null,?,?,?,?,?,?)'''
#                 cur.execute(statement,params)
#                 conn.commit()
#
#             except:
#                 pass



# # 2.3lyft data
client_id='KZ-TZqsDDPf9'
client_secret='K7GU9SoiwvUMcr-QyzQ_ynaqlGpEF9Ww'
access_token='7ze30S6B+qvt4f7vet2nm6PHg8q8wfQWEIg3lxeP1EPgHoLFagPZuevnqm07lXx19gwXZZMNdhwSRuCc2yVG+NacsXJifU3M8sJyjMavSvz1t6RpLCmL8u4='
scope= "public"
token_type='bearer'
#

auth_flow = ClientCredentialGrant(client_id, client_secret,scope,)
session = auth_flow.get_session()


client = LyftRidesClient(session)

#1.startpoint: nearby driver
user_input_address="San Francisco International Airport"
start_add=google_map.lat_log(user_input_address)

statement = """
SELECT e.lag_log
FROM EAT as e
"""
end_lag_log_list=cur.execute(statement).fetchall()


#
def estmate_cost(start,end,type="lyft"):
#     'https://api.lyft.com/v1/cost?start_lat=37.7763&start_lng=-122.3918&end_lat=37.7972&end_lng=-122.4533'
    s_lat=start.split(',')[0]
    s_log=start.split(',')[1]
    e_lat=end[0].split(',')[0]
    e_log=end[0].split(',')[1]

    cost_resp=client.get_cost_estimates(start_latitude=s_lat, start_longitude=s_log, end_latitude=e_lat, end_longitude=e_log).json
    est=cost_resp["cost_estimates"][0]

    est_dict={}
    est_dict['start']=start
    est_dict['end']=end
    est_dict['es_time']=est["estimated_duration_seconds"]/60


    est_dict['es_distance']=est["estimated_distance_miles"]

    est_dict['es_cost_max']=est["estimated_cost_cents_max"]/100
    est_dict['es_cost_min']=est["estimated_cost_cents_min"]/100

    return est_dict
#
#
#     query={}
#
#     query['start_lat']=s_lat
#     query['start_lng']=s_log
#     query['end_lat']=e_lat
#     query['end_lng']=e_log
#     query['ride_type']=type
#     AVAILABILITY="https://api.lyft.com/v1/cost?"
#     headers = {"Authorization": "{} {}".format(token_type,access_token)}
#     # query['headers']=headers
#     # cost_response = requests.get(AVAILABILITY,params=query, headers=headers)
#     cost_response = make_request_using_cache(AVAILABILITY,params=query)
#
#     print(cost_response[0])

#     est_dict={}
#     est_dict['start']=start
#     est_dict['end']=end
#     est_dict['es_time']=cost_text["cost_estimates"]["estimated_duration_seconds"]/60
#     est_dict['es_distance']=cost_text["cost_estimates"]["estimated_distance_miles"]
#     est_dict['es_cost_max']=cost_text["cost_estimates"]["estimated_cost_cents_max"]/100
#     est_dict['es_cost_min']=cost_text["cost_estimates"]["estimated_cost_cents_min"]/100
#
#     return est_dict
#
#
# {"cost_estimates": [{"ride_type": "lyft", "estimated_duration_seconds": 2831, "estimated_distance_miles": 15.69, "price_quote_id": "6a1106b3e29ae48a99026b2e68d1df26343b25442db0b2ad3b6224d4a950b95d", "estimated_cost_cents_max": 3805, "primetime_percentage": "0%", "is_valid_estimate": true, "currency": "USD", "cost_token": null, "estimated_cost_cents_min": 3805, "display_name": "Lyft", "primetime_confirmation_token": null, "can_request_ride": true}]}
#
for destination in end_lag_log_list:
    ridedb=estmate_cost(start_add,destination)
    param=(start_add,str(destination),ridedb['es_time'],ridedb['es_distance'],ridedb['es_cost_max'],ridedb['es_cost_min'])
    statement='''INSERT INTO RIDE VALUES(Null,?,?,?,?,?,?)'''
    cur.execute(statement,param)
    conn.commit()

# cost_resp=client.get_cost_estimates(start_latitude=37.7763, start_longitude=-122.3918, end_latitude=38.3918, end_longitude=-122.3918)
# print(cost_resp.json["cost_estimates"])
# cost=cost_resp.json
#
#
# eta_resp=client.get_eta(37.7763, -122.3918)


# 'https://api.lyft.com/v1/cost?start_lat=37.7763&start_lng=-122.3918&end_lat=37.7972&end_lng=-122.4533'
# #2. estimate to endpoint
# estimated_duration_seconds": 913,
#       "estimated_distance_miles": 3.29,
#       "estimated_cost_cents_max": 2355,
#       "primetime_percentage": "25%",
#       "currency": "USD",
#       "estimated_cost_cents_min": 1561,
#       "display_name": "Lyft Plus",
#       "primetime_confirmation_token": null,
#       "cost_token": null,
#       "is_valid_estimate": true


# response = client.get_ride_types(37.7833, -122.4167)
# ride_types = response.json.get('ride_types')
# ride_type=ride_types[0]
# 'https://api.lyft.com/v1/eta?lat=37.7763&lng=-122.3918'

#4.database

# from lyft.util.url_util import Availability
#
# from lyft.availability import Availability
# response = availability_obj.get_driver_eta(37.7763, -122.3918, 36.3452, -121.3435, 'lyft_line')
# print(response)

# class Availability(object):
#     def __init__(self, token_type, access_token):
#         self.token_type = token_type
#         self.__access_token = access_token
#
#     def get_ride_types(self, lat, lng, ride_type=None):
#         """
#         A GET to the /ridetypes endpoint returns the ride types available at the specified location,
#         indicated by latitude and longitude. If no ride types are available at the specified location,
#         the response will be an error.
#         :param lat: float, REQUIRED, Latitude of a location
#         :param lng: float, REQUIRED, Longitude of a location
#         :param ride_type: string, ID of a ride type. Returned by this endpoint
#         :return: ride types available in JSON format
#         """
#         # can use google map
#         lat = float(lat)
#         lng = float(lng)
#
#         if ride_type is None:
#             ride_types_url = "{}ridetypes?lat={}&lng={}".format(AVAILABILITY, lat, lng)
#         else:
#             ride_types_url = "{}ridetypes?lat={}&lng={}&ride_type={}".format(AVAILABILITY, lat, lng, ride_type)
#
#         headers = {"Authorization": "{} {}".format(self.token_type,
#                                                    self.__access_token)}
#
#         ride_types_available_response = requests.get(ride_types_url, headers=headers)
#
#         if ride_types_available_response.status_code == 200:
#             return ride_types_available_response.json()
#
#         else:
#             raise Exception(ride_types_available_response.json())
#
#     def get_driver_eta(self, lat, lng, end_lat=None, end_lng=None, ride_type=None):
#
#         lat = float(lat)
#         lng = float(lng)
#         # check if destination is given
#         if all([end_lat, end_lng]) is True:
#             end_lat = float(end_lat)
#             end_lng = float(end_lng)
#
#         # construct the request URL
#         if ride_type is None and (end_lat is None or end_lng is None):
#             driver_eta_url = "{}eta?lat={}&lng={}".format(AVAILABILITY, lat, lng)
#
#         elif ride_type is not None and (end_lat is None or end_lng is None):
#             driver_eta_url = "{}eta?lat={}&lng={}&ride_type={}".format(AVAILABILITY, lat, lng, ride_type)
#
#         elif ride_type is not None and (end_lat is not None or end_lng is not None):
#             driver_eta_url = "{}eta?lat={}&lng={}&end_lat={}&destination_lng={}&ride_type={}".format(
#                 AVAILABILITY, lat, lng, end_lat, end_lng, ride_type)
#
#         elif ride_type is None and (end_lat is not None or end_lng is not None):
#             driver_eta_url = "{}eta?lat={}&lng={}&end_lat={}&destination_lng={}".format(
#                 AVAILABILITY, lat, lng, end_lat, end_lng)
#
#         headers = {"Authorization": "{} {}".format(self.token_type,
#                                                    self.__access_token)}
#
#         driver_eta_response = requests.get(driver_eta_url, headers=headers)
#
#         if driver_eta_response.status_code == 200:
#             return driver_eta_response.json()
#
#         else:
#             raise Exception(driver_eta_response.json())
#
#     def get_ride_estimates(self, start_lat, start_lng, end_lat=None, end_lng=None, ride_type=None):
#         """
#         A GET to the /cost endpoint returns the estimated cost, distance, and duration of a ride between
#         a start location and end location. A success response will be broken down by ride types available
#         at the specified location. An optional ride_type parameter can be specified to only return the
#         cost_estimate for that ride_type. Valid inputs for the ride_type parameter can be found by querying
#         the /v1/ridetypes endpoint.
#         If the destination parameters are not supplied, the cost endpoint will simply return the Prime Time
#         pricing at the specified location.
#         :param start_lat: float, REQUIRED, Latitude of a location
#         :param start_lng: float, REQUIRED, Longitude of a location
#         :param end_lat: float, Latitude of a location
#         :param end_lng: float, Longitude of a location
#         :param ride_type: string, ID of a ride type. Returned by this endpoint
#         :return: ride estimates in JSON format
#         """
#         start_lat = float(start_lat)
#         start_lng = float(start_lng)
#         # check if destination is given
#         if all([end_lat, end_lng]) is True:
#             end_lat = float(end_lat)
#             end_lng = float(end_lng)
#
#         # construct the request URL
#         if ride_type is None and (end_lat is None or end_lng is None):
#             ride_estimates_url = "{}cost?start_lat={}&start_lng={}".format(AVAILABILITY,start_lat, start_lng)
#
#         elif ride_type is not None and (end_lat is None or end_lng is None):
#             ride_estimates_url = "{}cost?start_lat={}&start_lng={}&ride_type={}".format(AVAILABILITY,start_lat, start_lng, ride_type)
#
#         elif ride_type is not None and (end_lat is not None or end_lng is not None):
#             ride_estimates_url = "{}cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}&ride_type={}".format(
#                 AVAILABILITY, start_lat, start_lng, end_lat, end_lng, ride_type)
#
#         elif ride_type is None and (end_lat is not None or end_lng is not None):
#             ride_estimates_url = "{}cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}".format(
#                 AVAILABILITY, start_lat, start_lng, end_lat, end_lng)
#
#         headers = {"Authorization": "{} {}".format(self.token_type,
#                                                    self.__access_token)}
#
#         ride_estimates_response = requests.get(ride_estimates_url, headers=headers)
#
#         if ride_estimates_response.status_code == 200:
#             return ride_estimates_response.json()
#
#         else:
#             raise Exception(ride_estimates_response.json())
#
#     def get_nearby_drivers(self, lat, lng):
#         """
#         A GET to the /drivers endpoint returns the location of drivers near a location.
#         The result will contain a list of 5 locations for a sample of drivers for each ride type available
#         at the specified latitude and longitude.
#         :param lat: float, REQUIRED, Latitude of a location
#         :param lng: float, REQUIRED, Longitude of a location
#         :return: nearby drivers in JSON format
#         """
#         lat = float(lat)
#         lng = float(lng)
#
#         nearby_drivers_url = "{}drivers?lat={}&lng={}".format(AVAILABILITY, lat, lng)
#
#         headers = {"Authorization": "{} {}".format(self.token_type,
#                                                    self.__access_token)}
#
#         nearby_drivers_response = requests.get(nearby_drivers_url, headers=headers)
#
#         if nearby_drivers_response.status_code == 200:
#             return nearby_drivers_response.json()
#
#         else:
#             raise Exception(nearby_drivers_response.json())
#
#     def get_eta_and_nearby_drivers(self, lat, lng, end_lat=None, end_lng=None, ride_type=None):
#         """
#         A GET to the /nearby-drivers-pickup-etas endpoint returns the estimated time for nearby
#         drivers to reach the specified location, and their most recent locations.
#         A success response will be broken down by ridetypes available at the specified location.
#         An optional ride_type parameter can be specified to only return the ETA for that ridetype.
#         Valid inputs for the ride_type parameter can be found by querying the /v1/ridetypes endpoint.
#         An empty response indicates that the specified ride_type isn't available at the specified location.
#         You can try requesting again without the ride_type parameter.
#         :param lat: float, REQUIRED, Latitude of a location
#         :param lng: float, REQUIRED, Longitude of a location
#         :param end_lat: float, Latitude of a location
#         :param end_lng: float, Longitude of a location
#         :param ride_type: string, ID of a ride type. Returned by this endpoint
#         :return: nearby drivers and eta in JSON format
#         """
#         lat = float(lat)
#         lng = float(lng)
#         # check if destination is given
#         if all([end_lat, end_lng]) is True:
#             end_lat = float(end_lat)
#             end_lng = float(end_lng)
#
#         # construct the request URL
#         if ride_type is None and (end_lat is None or end_lng is None):
#             eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}".format(AVAILABILITY, lat, lng)
#
#         elif ride_type is not None and (end_lat is None or end_lng is None):
#             eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&ride_type={}".format(
#                 AVAILABILITY, lat, lng, ride_type)
#
#         elif ride_type is not None and (end_lat is not None or end_lng is not None):
#             eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&destination_lat={}&destination_lng={}&ride_type={}".format(
#                 AVAILABILITY, lat, lng, end_lat, end_lng, ride_type)
#
#         elif ride_type is None and (end_lat is not None or end_lng is not None):
#             eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&destination_lat={}&destination_lng={}".format(
#                 AVAILABILITY, lat, lng, end_lat, end_lng)
#
#         headers = {"Authorization": "{} {}".format(self.token_type,
#                                                    self.__access_token)}
#
#         eta_and_nearby_drivers_response = requests.get(eta_and_nearby_drivers_url, headers=headers)
#
#         if eta_and_nearby_drivers_response.status_code == 200:
#             return eta_and_nearby_drivers_response.json()
#
#         else:
#             raise Exception(eta_and_nearby_drivers_response.json())
#
# Availability().get_nearby_drivers(111,'123','45')
# 2.scraping +crawling
# baseurl="https://finance.yahoo.com/"
# industry_url=baseurl+"industries"
# html=make_request_using_cache(industry_url)
#
# soup = BeautifulSoup(html, 'html.parser')
# # select industry
# # print(soup.prettify())
# industry_col=soup.find_all('div',title=" Finance")
# industry_title_all=soup.find_all('a',class_="D(b) Td(n) Ta(start) C(black) Lh(34px)")
# print(industry_title_all)
# industry_url=find('a',title=)['href']


# openfile=
# header={'','','','','','',''}
# 3.database
#
# with open (CACHE_FNAME) as f
#     bars_dr=csv.reader(f)
#     bars_ls=[]
conn.close()
