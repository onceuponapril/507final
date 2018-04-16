
from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import json
import urllib
from urllib.parse import urlencode
import fn

CACHE_FNAME = 'trycache.json'
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

DBNAME='test_Foddie_Go.sqlite'
conn = sqlite3.connect(DBNAME,check_same_thread=False)
cur = conn.cursor()
map_api='AIzaSyCDFrR1bowszXuQLUG8f3pj61Q_Uc_mnzA'
class google_map():
    DBNAME='Foddie_Go.sqlite'
    conn = sqlite3.connect(DBNAME,check_same_thread=False)
    cur = conn.cursor()

    def __init__(self,address):
        self.addr=address

    def lat_log(self):

        map_url='https://maps.googleapis.com/maps/api/place/textsearch/json'
        params={}
        params['key']=map_api
        params['query']=str(self.addr)
        req=make_request_using_cache(map_url,params=params)
        rstxt=json.loads(req)
        rs=rstxt['results']
        geoloc=rs[0]['geometry']['location']

        lat=geoloc['lat']
        log=geoloc['lng']
        loc="{},{}".format(lat,log)

        return loc

statement = '''
    DROP TABLE IF EXISTS 'EAT';
'''
cur.execute(statement)

statement='''CREATE TABLE EAT(
'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
'City' TEXT NOT NULL,
'Name' TEXT NOT NULL,
'Price' TEXT,
'Rating' NUMERIC,
'address' TEXT,
'lag_log' TEXT
)'''
cur.execute(statement)
conn.commit()
# statement='SELECT * FROM EAT where EAT.City='+"'"+str(user_input_city)+"'"
# datalist=cur.execute(statement).fetchall()
# print(type(datalist))
# dt=fn.eat.get_eat_data(user_input_city)
# print(dt)

# class Yelpeat():
#     DBNAME='Foddie_Go.sqlite'
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()
#
#     def __init__(self,user_input_city):
#         user_input=user_input_city
#
# def get_data(user_input):
# # user_input_city='San Francisco'
#         statement='SELECT * FROM EAT where EAT.City='+"'"+str(user_input)+"'"
#         datalist=cur.execute(statement).fetchall()
#         if datalist !=[]:
#                 return datalist
#         else:

def get_data(user_input):
    baseurl="https://www.yelp.com/"
    search_url=baseurl+'search'
    param={}
    param['find_desc']="Top+100+Places+to+Eat"
    param['find_loc']=user_input
    n=range(5)
    for i in n:
                param['start']=i*10
                html=make_request_using_cache(search_url,param)
                soup_a = BeautifulSoup(html, 'html.parser')
                list_of_eat=soup_a.find_all("li",class_="regular-search-result")

                for eat in list_of_eat:
                    try:
                        name=eat.find('a',class_='biz-name').text.strip()
                        price=eat.find('span',class_="business-attribute price-range").text.strip()
                        rating=eat.find('div',class_='i-stars')['title'][:3]
                        add=eat.find('address').text.strip()
                        lat_log=google_map(add).lat_log()
                        print(name)

                        params=(user_input,name,price,rating,add,lat_log)
                        statement='''INSERT INTO EAT VALUES(Null,?,?,?,?,?,?)'''
                        cur.execute(statement,params)
                        conn.commit()

                    except:
                            pass




# print(get_data('Ann Arbor'))
# statement='SELECT * FROM EAT where EAT.City='+"'"+str(user_input)+"'"
# datalist=cur.execute(statement).fetchall()
# print(datalist)
# print(Yelpeat("San Francisco").get_data())

# clent_key='QRvco0EQ2P7iuEryoeIkuC0s1IlGIL5fb1jP9TaI'
# servertoken='aZS6nwgn0PhC7Q5jQjv5qbkB9UPNLVuGCsR_tQEi'
# session = Session(server_token=servertoken)
# client = UberRidesClient(session)
#
# response = client.get_products(37.77, -122.41)
# products = response.json.get('products')
#
# response = client.get_price_estimates(
#     start_latitude=37.770,
#     start_longitude=-122.411,
#     end_latitude=37.791,
#     end_longitude=-122.405,
#     seat_count=2
# )
#
# estimate = response.json.get('prices')
# print(estimate)

# response = client.get_user_profile()
# profile = response.json
#
# first_name = profile.get('first_name')
# last_name = profile.get('last_name')
# email = profile.get('email')
# from requests_oauthlib import OAuth1Session
# import secrets
#
#
#
# client_id=secrets.client_id
# client_secret=secrets.client_secret
# token_type='bearer'
# access_token=secrets.access_token
#
#  # "2-legged" flow auth
#
# from requests.auth import HTTPBasicAuth
# # from lyft.authentication import LyftPublicAuth
#
# header = {"content-type": "application/json"}
# # tokenurl='https://api.lyft.com/oauth/token'
# # requests.get(tokenurl)
# from requests.auth import HTTPBasicAuth
#
# # from lyft.util.url_util import PUBLIC_AUTH_URL
# auth=https://api.lyft.com/oauth/token
# authentication_response = requests.post(PUBLIC_AUTH_URL,
#                                                 headers=header,
#                                                 data=json.dumps(data),
#                                                 auth=HTTPBasicAuth(client_id, client_secret))
#
# if authentication_response.status_code == 200:
#             authentication_response_json = authentication_response.json()
#             resp= {"x-ratelimit-limit"     : authentication_response.headers.get("x-ratelimit-limit"),
#                     "x-ratelimit-remaining" : authentication_response.headers.get("x-ratelimit-remaining"),
#                     "expires_in"            : authentication_response_json.get("expires_in"),
#                     "access_token"          : authentication_response_json.get("access_token"),
#                     "token_type"            : authentication_response_json.get("token_type")}
#             print(resp)
#
# else:
#          print(authentication_response.json())
#refresh
# from lyft.session import Session
# session_obj = Session({"client_id": client_id, "client_secret": client_secret}, refresh_token, sandbox_mode=True/False}
# session_obj.refresh_access_token()
# 	# to revoke token
# 	session_obj.revoke_token()

# 1.	The data sources you intend to use, along with your self-assessment of the “challenge score” represented by your data source selection.
# I want to scrap the data from yahoo finance website, which satisfied the requirement of “Crawling [and scraping] multiple pages in a site you haven’t used before” (9pt).
#
# 2.	The presentation options you plan to support (what information will be displayed)
# I would like to display the current price, market capital, price change, volumn and Avg vol of first 100 companies in the industry the user input. Also, user can check one company’s financials data.
#
# 3.	The presentation tool(s) you plan to use.
# I would like to use plotly: histogram, line plot, scatter plot, bar chart
# It would be much better if you could make your program distinct from other similar tools. Also, consider how you would display them more in detail (not just histogram, bar chart, ect)


#1.cache




# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()
#
# except:
#     CACHE_DICTION = {}
#
# def get_unique_key(url):
#     return url
#
# def make_request_using_cache(url):
#     unique_ident = get_unique_key(url)
#
#     if unique_ident in CACHE_DICTION:
#         print("Getting cached data...")
#         return CACHE_DICTION[unique_ident]
#
#     else:
#         print("Making a request for new data...")
#
#
#         resp = requests.get(url)
#         CACHE_DICTION[unique_ident] = resp.text
#         dumped_json_cache = json.dumps(CACHE_DICTION)
#         fw = open(CACHE_FNAME,"w")
#         fw.write(dumped_json_cache)
#         fw.close()
#         return CACHE_DICTION[unique_ident]

# # lyft data
# from lyft.util.url_util import AVAILABILITY


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


# user_input='San Francisco'
# baseurl="https://www.yelp.com/"
# search_url=baseurl+'search'
# param={}
# param['find_desc']="Top+100+Places+to+Eat"
# param['find_loc']=user_input
# n=range(10)
# for i in n:
#     param['start']=i*10
#     html=make_request_using_cache(search_url,param)
#     soup_a = BeautifulSoup(html, 'html.parser')
#
#     pages=soup_a.find_all('a',class_='available-number pagination-links_anchor')
#     for each in pages:
#         newpage=each['href']
#         new_url=baseurl+newpage
# # # #2.scrap
#     new_html=make_request_using_cache(new_url)
#     soup_b = BeautifulSoup(new_html, 'html.parser')
#     list_of_eat=soup_b.find_all("li",class_="regular-search-result")
#
#     for eat in list_of_eat[:2]:
#         try:
#             name=eat.find('a',class_='biz-name').text.strip()
#
#         except:
#             pass
#
#         try:
#             address=eat.find('address').text.strip()
#         except:
#             pass
#
#         try:
#             address=eat.find('address').text.strip()
#         except:
#             pass
#
#         try:
#                 address=eat.find('address').text.strip()
#         except:
#                 pass
#
#         try:
#             phone=eat.find('span',class_='biz-phone').text.strip()
#         except:
#             pass
#
#         try:
#             price=eat.find('span',class_="business-attribute price-range").text.strip()
#         except:
#             pass
#
#         try:
#             rating=eat.find('div',class_='i-stars')['title']
#         except:
#             pass
#
#         loc=google_map(address)
#         lat=google_map(address)
# #
# final_url=search_url+'$start=90'
# final_html=make_request_using_cache(final_url,param)
#
# soup_a = BeautifulSoup(html, 'html.parser')
# final_list_of_eat=soup_a.find_all("li",class_="regular-search-result")
# db_list={}
# for eat in first_list_of_eat:
#     name=eat.find('a',class_='biz-name').text.strip()
#     address=eat.find('address').text.strip()
#     phone=eat.find('span',class_='biz-phone').text.strip()
#     price=eat.find('span',class_="business-attribute price-range").text.strip()
#     # loc=google_map(address)
#     # lat=google_map(address)

# WRITE INTO DB

        # except:
        #     pass








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
