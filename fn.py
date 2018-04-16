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


#2 Create DB
# 3 WRITE INTO DB

DBNAME='Foddie_Go.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
# #
# statement = '''
#     DROP TABLE IF EXISTS 'EAT';
# '''
# cur.execute(statement)

# statement = '''
#     DROP TABLE IF EXISTS 'RIDE';
# '''
# cur.execute(statement)

# statement='''CREATE TABLE EAT(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'City' TEXT NOT NULL,
# 'Name' TEXT NOT NULL,
# 'Price' TEXT,
# 'Rating' NUMERIC,
# 'address' TEXT,
# 'lag_log' TEXT
# )'''
# cur.execute(statement)
# conn.commit()

# statement='''CREATE TABLE LIMITED_RIDE(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'Origin'TEXT NOT NULL,
# 'Origin_geo' TEXT,
# 'Destination' TEXT,
# 'Destination_geo' TEXT,
# 'Estimated_time(minute)' TEXT,
# 'Estimated_distance(miles)' TEXT,
# 'Estimated_max_cost(dollar)' TEXT,
# 'Estimated_min_cost(dollar)' TEXT)
# '''
# cur.execute(statement)
# conn.commit()
#
#

# 3.1 google maps
class google_map():
    def __init__(self,address):
        self.addr=address

    def lat_log(self,address):

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




# 3. yelp data
# statement='''CREATE TABLE EAT(
# 'Id' INTEGER NULL PRIMARY KEY AUTOINCREMENT,
# 'City' TEXT NOT NULL,
# 'Name' TEXT NOT NULL,
# 'Price' TEXT,
# 'Rating' NUMERIC,
# 'address' TEXT,
# 'lag_log' TEXT
# )'''
# cur.execute(statement)
# conn.commit()

# user_input_city='San Francisco'
class Yelpeat():
    DBNAME='Foddie_Go.sqlite'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    def __init__(self,user_input_city):
        self.city=user_input_city

    def get_data(self):
# user_input_city='San Francisco'
        statement='SELECT * FROM EAT where EAT.City='+"'"+str(self.city)+"'"
        datalist=cur.execute(statement).fetchall()
        if datalist !=[]:
                return datalist
        else:
            self.create_db()
            statement='SELECT * FROM EAT where EAT.City='+"'"+str(self.city)+"'"
            statement+=' LIMIT 100'
            datalist=cur.execute(statement).fetchall()
            return datalist

    def create_db(self):

                baseurl="https://www.yelp.com/"
                search_url=baseurl+'search'
                param={}
                param['find_desc']="Top+100+Places+to+Eat"
                param['find_loc']=self.city
                n=range(12)
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
                                    price=eat.find('span',class_="business-attribute price-range").text.strip()
                                    rating=eat.find('div',class_='i-stars')['title'][:3]
                                    add=eat.find('address').text.strip()
                                    lat_log=google_map.lat_log(add)
                                    count+=1

                                    params=(self.city,name,price,rating,add,lat_log)
                                    statement='''INSERT INTO EAT VALUES(Null,?,?,?,?,?,?)'''
                                    cur.execute(statement,params)
                                    conn.commit()

                                except:
                                        pass



print(len(Yelpeat("Ann Arbor").get_data()))


# class lyft_data():
#     def estmate_cost(start,end,type="lyft"):
#         client_id='KZ-TZqsDDPf9'
#         client_secret='K7GU9SoiwvUMcr-QyzQ_ynaqlGpEF9Ww'
#         access_token='7ze30S6B+qvt4f7vet2nm6PHg8q8wfQWEIg3lxeP1EPgHoLFagPZuevnqm07lXx19gwXZZMNdhwSRuCc2yVG+NacsXJifU3M8sJyjMavSvz1t6RpLCmL8u4='
#         scope= "public"
#         token_type='bearer'
#         auth_flow = ClientCredentialGrant(client_id, client_secret,scope,)
#         session = auth_flow.get_session()
#         client = LyftRidesClient(session)
#
#         s_lat=start.split(',')[0]
#         s_log=start.split(',')[1]
#         e_lat=end.split(',')[0]
#         e_log=end.split(',')[1]
#         # e_lat=end[0].split(',')[0]
#         # e_log=end[0].split(',')[1]S
#
#         est_dict={}
#         try:
#             cost_resp=client.get_cost_estimates(start_latitude=s_lat, start_longitude=s_log, end_latitude=e_lat, end_longitude=e_log).json
#             est=cost_resp["cost_estimates"][0]
#
#             est_dict['start']=start
#             est_dict['end']=end
#             est_dict['es_time']=est["estimated_duration_seconds"]/60
#             est_dict['es_distance']=est["estimated_distance_miles"]
#             est_dict['es_cost_max']=est["estimated_cost_cents_max"]/100
#             est_dict['es_cost_min']=est["estimated_cost_cents_min"]/100
#         except:
#             est_dict['start']=start
#             est_dict['end']=end
#             est_dict['es_time']='Not avaliable'
#             est_dict['es_distance']='Not avaliable'
#             est_dict['es_cost_max']='Not avaliable'
#             est_dict['es_cost_min']='Not avaliable'
#
#         return est_dict
#
#     def create_table():
#         user_input_address="San Francisco International Airport"
#         statement = 'SELECT Address FROM EAT LIMIT 100'
#         end_list=cur.execute(statement).fetchall()
#
#         start_add=google_map.lat_log(user_input_address)
#         for each in end_list:
#             end_add=google_map.lat_log(str(each).strip('()'))
#             ridedb=estmate_cost(start_add,end_add)
#             param=(user_input_address,start_add,ridedb['es_time'],ridedb['es_distance'],ridedb['es_cost_max'],ridedb['es_cost_min'])
#             statement='''INSERT INTO LIMITED_RIDE VALUES(Null,?,?,NULL,Null,?,?,?,?)'''
#             cur.execute(statement,param)
#             conn.commit()
#
#         update_one='UPDATE LIMITED_RIDE SET Destination_geo=(SELECT lag_log FROM EAT where LIMITED_RIDE.Id=EAT.Id)'
#         cur.execute(update_one)
#         conn.commit()
#
#         update_two='UPDATE LIMITED_RIDE SET Destination=(SELECT Address FROM EAT where LIMITED_RIDE.Id=EAT.Id)'
#         cur.execute(update_two)
#         conn.commit()


# conn.close()

#4 Interactive presentation
# from flask import Flask, render_template, request
# 1.user input city and number of resturant wanna check--TABLE
# 2. sort by rating and price- choose resturants--TABLE
# 3.INPUT YOUR ORIGIN--TABLE:ESTIMATION
#4.MAP

# 1.user input city and number of resturant wanna check--TABLE
