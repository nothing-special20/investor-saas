from modulefinder import replacePackageMap
import re
import json
import sys
import os

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import TemporaryUploadedFile

from .models import ParcelCoordinates

google_maps_api_key = os.getenv('GOOGLE_MAPS_API')

#Twilio
from twilio.rest import Client
import googlemaps

def address_builder(record):
    address = record['ADDR_1']
    city = record['CITY']
    state = record['STATE']
    zip_code = record['ZIP']
    return ' '.join([address, city, state, zip_code])

def get_coordinates(address):
    gmaps = googlemaps.Client(key=google_maps_api_key)
    result = json.dumps(gmaps.geocode(address))
    result2 = json.loads(result)
    latitude = result2[0]['geometry']['location']['lat']
    longitude = result2[0]['geometry']['location']['lng']
    context = {
        'result':result,
        'latitude':latitude,
        'longitude':longitude,
        'title': address
    }

    return context

def coordinates(record):
    try:
        obj = list(ParcelCoordinates.objects.filter(PIN=record['PIN']).values())
        print(obj)
        context = {
            'latitude': obj[0]['LATITUDE'],
            'longitude':obj[0]['LONGITUDE'],
            'title': address_builder(record)
        }
        print('fetched coords from database')
        return context

    except:
        address = address_builder(record)
        context = get_coordinates(address)
        print('fetched coords from google')

        doc = ParcelCoordinates(PIN=record['PIN'],
                                FOLIO=record['FOLIO'], 
                                LATITUDE=context['latitude'], 
                                LONGITUDE=context['longitude'],
                                COUNTY=record['COUNTY'])
        doc.save()
        return context

def twilio_sms(to_num, msg):
    # Your Account SID from twilio.com/console
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    # Your Auth Token from twilio.com/console
    auth_token  = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_num,
        from_="+18645280195",
        body=msg)

    print(message.sid)


def mock_data(category='', setIndex=None):
    data = [
        {
            'firstName': 'Kevin',
            'lastName': 'Smith',
            'phone': '813-434-0720',
            'email': 'whatever122@mailinator.com',
            'category': 'Cold Leads'
        },
        {
            'firstName': 'James',
            'lastName': 'Smith',
            'phone': '813-434-0720',
            'email': 'whatever92@mailinator.com',
            'category': 'Cold Leads'
        },
        {
            'firstName': 'Brett',
            'lastName': 'Contreras',
            'phone': '813-434-0720',
            'email': 'whatever92@mailinator.com',
            'category': 'Cold Leads'
        },
        {
            'firstName': 'Anderson',
            'lastName': 'Silva',
            'phone': '813-434-0720',
            'email': 'thebeast@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Vince',
            'lastName': 'Gold',
            'phone': '813-434-0720',
            'email': 'vincegold@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Alex',
            'lastName': 'Persian',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Anthony',
            'lastName': 'Garcia',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Tony',
            'lastName': 'Soprano',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Anderson',
            'lastName': 'Silva',
            'phone': '813-434-0720',
            'email': 'thebeast@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Vince',
            'lastName': 'Gold',
            'phone': '813-434-0720',
            'email': 'vincegold@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Alex',
            'lastName': 'Persian',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Anthony',
            'lastName': 'Garcia',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            'firstName': 'Tony',
            'lastName': 'Soprano',
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Requested Quotes'
        },
        {
            "firstName": "Marcus",
            "lastName": "Eurysaces",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Lucius",
            "lastName": "Jucundus",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Livia",
            "lastName": "Drusilla",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Gaius",
            "lastName": "Caesar",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Allia",
            "lastName": "Potestas",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Publius",
            "lastName": "Potestas",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Margaret",
            "lastName": "Thatcher",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Calls'
        },
        {
            "firstName": "Alexander",
            "lastName": "the Great",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Georgios",
            "lastName": "Papanikolaou",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Theodoros",
            "lastName": "Kolokotronis",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Constantine",
            "lastName": "Karamanlis",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Eleftherios",
            "lastName": "Venizelos",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Ioannis",
            "lastName": "Kapodistrias",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Scheduled Appointments'
        },
        {
            "firstName": "Frederick",
            "lastName": "the Great",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        },
        {
            "firstName": "Otto",
            "lastName": "von Bismarck",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        },
        {
            "firstName": "Johannes",
            "lastName": "Gutenberg",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        },
        {
            "firstName": "Martin",
            "lastName": "Luther",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        },
        {
            "firstName": "Johann",
            "lastName": "Sebastian Bach",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        },
        {
            "firstName": "Johann",
            "lastName": "Wolfgang Goetheis",
            'phone': '813-434-0720',
            'email': 'xerxes@mailinator.com',
            'category': 'Closed Deals'
        }
        ]

    if category!='':
        data = [x for x in data if category==x['category']]

    index = 0
    for x in data:
        x['index'] = index
        index += 1

    if setIndex is not None:
        data = [x for x in data if setIndex==x['index']]
    return data


