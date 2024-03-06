import random
import time
import requests
import json

def location_bd(address):
    base_url = "http://api.map.baidu.com/geocoder?address={address}&output=json&key=yourKey".format(address=address)
    response = requests.get(base_url)
    answer = response.json()
    latitude = answer['result']['location']['lat']
    longitude = answer['result']['location']['lng']
    return [longitude,latitude]


def get_d_name(address):
    info = {
    'stName': address,
    'type':'place',
    'page':1,
    'size':200,
    'year':2022,
    }

    headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    url = r'https://dmfw.mca.gov.cn/9095/stname/listPub'
    result = requests.post(url=url,data=info,headers=headers).json()
    return result

def location_gd(address):
    base_url = 'https://restapi.amap.com/v3/geocode/geo?key=yourKey&address={address}'.format(address=address)
    response = requests.get(base_url)
    answer = response.json()
    if answer['status'] == '1':
        location = answer['geocodes'][0]['location'].split(',')
        latitude = float(location[1])
        longitude = float(location[0])
        return [longitude,latitude]
