from django.shortcuts import render
import requests
from django.http import JsonResponse
import json


# Numbeo api documentation : https://www.numbeo.com/api/doc.jsp

# Create your views here.
def getCostOfLiving(request, city, state):
    key = json.load(open('./API_KEYS.json'))["numbeo"]
    #url = f'/api/?api_key={key}&query={lon},{lat}&min_contributors=5&max_distance=10000'
    #cityName = 'Example'
    #state = 'Example
    print(city, state)
    url = f'https://www.numbeo.com/api/city_prices?api_key={key}&query={city},%20{state}'
    print("--------------------------")
    print(url)
    print("--------------------------")

    r = requests.get(url)
    stuff = r.json()

    return JsonResponse(stuff)
