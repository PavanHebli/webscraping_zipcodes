import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import time
from itertools import cycle
import os
import random

proxy = open("proxies and ports List.txt","r")
proxy= proxy.read()
proxyList=proxy.split("\n")
loopingOverIP = cycle(proxyList)
samplex=0
def proxyIP(loopOBJ=loopingOverIP):
    currenIP = next(loopOBJ)
    global samplex
    while True:
        try:
            print("going to get response")
            response=requests.get("http://icanhazip.com",proxies={"http":currenIP,"https":currenIP},timeout=20)
            print("response is here")
            if response.status_code == 200:
                samplex=0
                return currenIP
            else:
                print("Try Else: "+response)
        except:
            currenIP = next(loopOBJ)
            if samplex == 8:
                samplex=0
                return None
            print(samplex)
            samplex= samplex+1

def locator(locate_zipcode):
    try:
        #var_proxyIP=proxyIP()
        locator = Nominatim(user_agent='geopy/1.21.0',proxies={"https":proxyIP()})
        location = locator.geocode(locate_zipcode)
        testString="locator using proxy ip"
    except:
        locator = Nominatim(user_agent="GeoCoding")
        location = locator.geocode(locate_zipcode)
        testString="locator() using local ip"
    return location,testString

def GetZipCode(expression,stateproxy,cityproxy,statename,cityname,zipcodeproxy=None,test=0):
    # try:
    #     geocode,testString=locator(expression)
    #     writeToFile.writelines("{}, {}, {}, {}, {}".format(test,expression,geocode.latitude,geocode.longitude,testString))
    #     print("{}, {}, {}, {}, {}".format(test,expression,geocode.latitude,geocode.longitude,testString))
    #     #print("{}".format(test),expression)
    # except:
    #     geocode,testString=locator(expression)
    #     writeToFile.writelines("{}, {}, {}, {}, {}".format(test,expression, "no longitude lattitude",testString))
    #     print("{}, {}, {}, {}, {}".format(test,expression,geocode.latitude,geocode.longitude,testString))
    # with open("united-states.txt","a") as file_object:
    #     file_object.writelines("{}".format(expression))
    return "{} {} {} {} {} {} {}\n".format(test,stateproxy,cityproxy,statename,cityname,expression,zipcodeproxy)


countryName="united-states"#input("enter the country name please= ")
URL = 'https://worldpostalcode.com/'+countryName.lower()+'/'
currenIP=proxyIP()
if os.path.exists(countryName+".txt"):
    os.remove(countryName+".txt")
try:
    state = requests.get(URL,proxies={"https":currenIP},timeout=30)
    print("state using proxy")
    stateproxy="state using proxy"
except:
    state = requests.get(URL,timeout=30)
    print("state using no proxy")
    stateproxy="state using no proxy"
#
# writeToFile= open(countryName+".txt","a")
StateBS = BeautifulSoup(state.content, 'html.parser')
results = StateBS.find(class_='regions')
for StateURL in results:
    print(StateURL.text)
    cityURL='https://worldpostalcode.com'+StateURL["href"]
    try:
        city=requests.get(cityURL,proxies={"https":currenIP},timeout=30)
        print("city using proxy")
        cityproxy="city using proxy"
    except:
        city=requests.get(cityURL,timeout=30)
        print("city using no proxy")
        cityproxy="city using no proxy"
    city_HTML_OBJ=BeautifulSoup(city.content, 'html.parser')
    CityName=city_HTML_OBJ.find(class_='regions')
    zipcodeVar=None
    latitudeVar=None
    longitudeVar=None
    if CityName == None:
        zipcodeInfo=city_HTML_OBJ.find(class_='codes')
        zipcode=zipcodeInfo.find_all(class_="code")
        for zips in zipcode:
            if len(zips.text) > 5:
                for singleZip in (zips.text).split(" "): 
                    with open("united-states.txt","a") as file_object:
                        file_object.write(GetZipCode (singleZip,stateproxy=stateproxy,cityproxy=cityproxy,statename=StateURL.text,cityname="-",test=1))
                    # GetZipCode (singleZip,test=1)
            else:
                with open("united-states.txt","a") as file_object:
                    file_object.write(GetZipCode (zips.text,stateproxy=stateproxy,cityproxy=cityproxy,statename=StateURL.text,cityname="-",test=2))
                #GetZipCode (zips.text,test=2)
    else:
        for Name in CityName:
            print("--"+Name.text)
            zipURL='https://worldpostalcode.com'+Name["href"]
            try:
                zipCode=requests.get(zipURL,proxies={"https":currenIP},timeout=30)
                print("zipcode using proxy")
                zipcodeproxy="zipcode using proxy"
            except:
                zipCode=requests.get(zipURL,timeout=10)
                print("zipcode using no proxy")
                zipcodeproxy="zipcode using no proxy"
            zip_HTML_OBJ=BeautifulSoup(zipCode.content, 'html.parser')
            zipcodeInfo=zip_HTML_OBJ.find(class_='codes')
            zipcode=zipcodeInfo.find_all(class_="code")
            for zips in zipcode:
                if len(zips.text) > 5:
                    for singleZip in (zips.text).split(" "):
                        with open("united-states.txt","a") as file_object:
                            file_object.write(GetZipCode (singleZip,stateproxy=stateproxy,cityproxy=cityproxy,statename=StateURL.text,cityname=Name.text,zipcodeproxy=zipcodeproxy,test=3))
                        #GetZipCode(singleZip,test=3)
                else:
                    with open("united-states.txt","a") as file_object:
                        file_object.write(GetZipCode (zips.text,stateproxy=stateproxy,cityproxy=cityproxy,statename=StateURL.text,cityname=Name.text,test=4))
                    #GetZipCode (zips.text,test=4)
            print("before calling proxy")
            currenIP=proxyIP()
            print("after calling proxy")
            time.sleep(1)
    #currenIP=proxyIP()
    time.sleep(1)
#print(results.prettify())


