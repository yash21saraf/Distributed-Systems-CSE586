from flask import Flask, render_template, jsonify, request
import requests
import gmaps
import json
import googlemaps
from datetime import datetime
from datetime import timedelta
import math
import polyline
import re
from key import mapkey
from key import weatherkey
import urllib.parse as urlparse
from urllib.parse import urlencode

### Included the MongoDB client and set port number to 27017
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

### Declared the weather API key and URL
weatherapi = weatherkey
weathercall = "http://api.openweathermap.org/data/2.5/weather?"

###Defined the database name and collections name
db = client.trial
##Stores the json respose of google maps
mapdata = db.mapdata
##Stores the weather data for all lat long pairs
wedata = db.wedata
##Stores and keeps records of all the requets made
arrreq = db.allreq


##GOOGLE MAPS AUTHENTICATION USING KEY
gmaps = googlemaps.Client(key=mapkey)
app = Flask(__name__)

##Render the page at the start up
@app.route('/')
def abcd():
    ###Defined all the blank variables and check as false to make sure some loops don't run on frontend
    check = "False"
    source = ""
    dest = ""
    temparr = ""
    tempplace = ""
    redcoord = ""
    sjson = ""
    ###Render the start page
    return render_template("index.html" , origin = source, destination = dest, temps = temparr,places = tempplace, coordarr = redcoord, check = check, serverjson = sjson)

###After the form has been submitted suing the post
@app.route('/', methods = ["POST"])
def abcd_abc():
    ### Get all the form data
    source = request.form['start']
    dest = request.form['end']

    now = datetime.now()
    t1 = datetime.now()
    ###Check if the same request exists in the databse
    if(mapdata.find_one({"startpos" : source, "endpos" : dest})):
            ###Obtain the request from the database and compare timestamp to present time
            ob_json =  mapdata.find_one({"startpos" : source, "endpos" : dest})
            timediff = ob_json["uptimestamp"] - now
            time_diff_hours = timediff / timedelta(hours=1)
            ###If the same request has been made in less than 24 hours than return the database request
            if (time_diff_hours < 24):
                dir_json = ob_json["dir_json"]
            else:
                ### If the time is greater than 24 hours, update databse by making a new api call
                mapdata.delete_one({"startpos" : source, "endpos" : dest})
                dir_json = gmaps.directions(str(source),
                                            str(dest),
                                            mode="driving",
                                            departure_time=now)
                dir_json = dir_json[0]
                myparam = {"startpos": source,
                           "endpos": dest,
                           "uptimestamp": now,
                           "dir_json" : dir_json
                           }
                result = mapdata.insert_one(myparam)

    else:
        ###If the request is not present in the databse then make a new call
        dir_json = gmaps.directions(str(source),
                                    str(dest),
                                    mode="driving",
                                    departure_time=now)
        dir_json = dir_json[0]
        myparam = {"startpos": source,
                   "endpos": dest,
                   "uptimestamp": now,
                   "dir_json" : dir_json
                   }

        result = mapdata.insert_one(myparam)

    ###Extract polyline from the maps respose
    poly = dir_json['overview_polyline']['points']
    coordinates = polyline.decode(poly)

    ###Since the response contains a lot of latlong pairs only 8 equispaced points will be used
    ### Reducing the space
    neededlen = math.floor(len(coordinates)/8)
    startcoord = coordinates[1]
    endcoord = coordinates[-1]
    counter = 1
    redcoord = []
    redcoord.append(startcoord)
    for coord in coordinates:
        if(counter%neededlen == 0):
            redcoord.append(coord)
        counter = counter + 1
    redcoord.append(endcoord)
    temparr = []
    tempplace = []

    ### Weather API hit by checking the databse
    for coord in redcoord:
        latdb = round(coord[0], 1)
        londb = round(coord[1], 1)
        ### If presesnt in database
        if(wedata.find_one({'lat' : latdb ,'lon' : londb})):
                we_json_temp =  wedata.find_one({'lat' : latdb ,'lon' : londb})
                timediff = we_json_temp["uptimestamp"] - now
                time_diff_hours = timediff / timedelta(hours=1)
                ### If the response has been made in last 6 hours return databse response
                if (time_diff_hours < 6):
                    temp = we_json_temp['temp']
                    place_name = we_json_temp['name']
                    temparr.append(temp)
                    tempplace.append(place_name)
                else:
                    ### Make new request and update in the databse
                    wedata.delete_one({'lat' : latdb ,'lon' : londb})
                    params = {'lat':coord[0],'lon':coord[1],'appid':weatherapi}
                    call = weathercall + urlencode(params)
                    weather = requests.get(call).json()

                    temp = weather['main']['temp']
                    place_name = weather['name']
                    temparr.append(temp)
                    tempplace.append(place_name)

                    myparams = {"lat": latdb,
                                "lon": londb,
                                "name" : place_name,
                                "temp" : temp,
                                "uptimestamp": now
                               }

                    result = wedata.insert_one(myparams)

        else:
                ###Make new request and update in the databse
                params = {'lat':coord[0],'lon':coord[1],'appid':weatherapi}
                call = weathercall + urlencode(params)
                # return call
                weather = requests.get(call).json()

                temp = weather['main']['temp']
                place_name = weather['name']
                temparr.append(temp)
                tempplace.append(place_name)

                myparams = {"lat": latdb,
                            "lon": londb,
                            "name" : place_name,
                            "temp" : temp,
                            "uptimestamp": now
                           }

                result = wedata.insert_one(myparams)

    check = "True"

    ###Update the entry in the databse
    myparams = {"source": source,
                "destination": dest,
                "place_name" : tempplace,
                "temprature" : temparr,
                "coordinates" : redcoord,
                "reqtimestamp": now
               }
    result = arrreq.insert_one(myparams)

    t2 = datetime.now()
    cost = (t2-t1).microseconds
    ### Pass all the variables to the frontend
    return render_template("index.html",origin = source, destination = dest, temps = temparr,places = tempplace, coordarr = redcoord, check = check, serverjson = dir_json, cost = cost  )

if __name__ == '__main__':
    app.run(debug=True)
