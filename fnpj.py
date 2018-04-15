import secrets
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
CACHE_FNAME = 'finalcache.json'
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
DBNAME='Foodie_Go.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
# #
# statement = '''
#     DROP TABLE IF EXISTS 'EAT';
# '''
# cur.execute(statement)
# #
# statement = '''
#     DROP TABLE IF EXISTS 'RIDE';
# '''
# cur.execute(statement)
#
# statement='''CREATE TABLE EAT(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'Name' TEXT NOT NULL,
# 'Phone' TEXT,
# 'Price' TEXT,
# 'Rating ' NUMERIC,
# 'Address' TEXT,
# 'Lag_log' TEXT
# )'''
# cur.execute(statement)
# conn.commit()



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
user_input='San Francisco'
baseurl="https://www.yelp.com/"
search_url=baseurl+'search'
param={}
param['find_desc']="Top+100+Places+to+Eat"
param['find_loc']=user_input
n=range(20)

count=0
while count<100:
    for i in n:
        param['start']=i*10
        html=make_request_using_cache(search_url,param)
        soup_a = BeautifulSoup(html, 'html.parser')
        list_of_eat=soup_a.find_all("li",class_="regular-search-result")

        for eat in list_of_eat:
            try:
                name=eat.find('a',class_='biz-name').text.strip()
                phone=eat.find('span',class_='biz-phone').text.strip()
                price=eat.find('span',class_="business-attribute price-range").text.strip()
                rating=eat.find('div',class_='i-stars')['title'][:3]
                add=eat.find('address').text.strip()
                lat_log=google_map.lat_log(add)
                count+=1

                params=(name,phone,price,rating,add,lat_log)
                statement='''INSERT INTO EAT VALUES(Null,?,?,?,?,?,?)'''
                cur.execute(statement,params)
                conn.commit()

            except:
                pass



# # 2.3lyft data
# statement='''CREATE TABLE RIDE(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'Origin'TEXT NOT NULL,
# 'Origin_geo' TEXT NOT NULL,
# 'Destination' TEXT NOT NULL,
# 'Destination_geo' TEXT NOT NULL,
# 'Estimated time (minute)' TEXT,
# 'Estimated distance(miles)' TEXT,
# 'Estimated maximun cost (dollar)' TEXT,
# 'Estimated minimum cost (dollar)' TEXT)
# '''
# cur.execute(statement)
# conn.commit()
#
# update_one='UPDATE RIDE SET Destination_geo=(SELECT lag_log FROM EAT)'
# cur.execute(update_one)
# conn.commit()
#
# update_two='UPDATE RIDE SET Destination=(SELECT address FROM EAT)'
# cur.execute(update_two)
# conn.commit()

client_id='KZ-TZqsDDPf9'
client_secret='K7GU9SoiwvUMcr-QyzQ_ynaqlGpEF9Ww'
access_token='7ze30S6B+qvt4f7vet2nm6PHg8q8wfQWEIg3lxeP1EPgHoLFagPZuevnqm07lXx19gwXZZMNdhwSRuCc2yVG+NacsXJifU3M8sJyjMavSvz1t6RpLCmL8u4='
scope= "public"
token_type='bearer'
#

auth_flow = ClientCredentialGrant(client_id, client_secret,scope,)
session = auth_flow.get_session()
client = LyftRidesClient(session)

#1.startpoint

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
#start address
user_input_address="San Francisco International Airport"
start_add=google_map.lat_log(user_input_address)
#destination address
statement='select Destination_geo from RIDE'
destination=cur.execute(statement).fetchall()
print(destination)
# for each in destination:
#     ridedb=estmate_cost(start_add,each)
#     param=(user_input_address,start_add,ridedb['es_time'],ridedb['es_distance'],ridedb['es_cost_max'],ridedb['es_cost_min'])
#     statement='''INSERT INTO RIDE(Origin, Origin_geo, Estimated time (minute), Estimated distance(miles),Estimated maximun cost (dollar),Estimated minimum cost (dollar))
#      VALUES(?,?,?,?,?,?)'''
#     cur.execute(statement,param)
#     conn.commit()


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
#
conn.close()



# if __name__ == '__main__':
#     # model.init_bball()
#     app.run(debug=True)
