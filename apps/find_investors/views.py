import os

import django
from django.shortcuts import render
from django.http import JsonResponse

from .functions import mock_data, twilio_sms, coordinates
from .models import ParcelInfo

import json

google_maps_api_key = os.getenv('GOOGLE_MAPS_API')

# Create your views here.

cold_leads = mock_data('Cold Leads')
requested_quotes = mock_data('Requested Quotes')
scheduled_calls = mock_data('Scheduled Calls')
scheduled_appointments = mock_data('Scheduled Appointments')
closed_deals = mock_data('Closed Deals')

categories = list(set([x['category'] for x in mock_data()]))
category_data = []

for x in categories:
    data = mock_data(x)
    output = {
                'name': x, 
                'data': data,
                'count': len(data)
                }
    category_data.append(output)

misc_values = {
        'categories': category_data,
        'cold_leads_count': len(cold_leads),
        'cold_leads': cold_leads,
        'requested_quotes_count': len(requested_quotes),
        'requested_quotes': requested_quotes,
        'scheduled_calls_count': len(scheduled_calls),
        'scheduled_calls': scheduled_calls,
        'scheduled_appointments_count': len(scheduled_appointments),
        'scheduled_appointments': scheduled_appointments,
        'closed_deals_count': len(closed_deals),
        'closed_deals': closed_deals,
        'msgBody': '',
        'msgSubject': ''   
    }

def send_message(request):
    if request.user.is_authenticated:
        print(request.POST)
        index = request.POST.get('index').split('~')
        category = index[0]
        index_num = int(index[1])
        print(index)
        data = mock_data(category, index_num)[0]
        first_name = data['firstName']
        phone = data['phone']
        msg = first_name + ' ' + misc_values['msgBody']
        twilio_sms(phone, msg)
        return find_investors(request)
    
    else:
        return render(request, 'web/landing_page.html')

def geocode(request):
    # gmaps = googlemaps.Client(key=google_maps_api_key)
    # result = json.dumps(gmaps.geocode(str('The Sundial, 2nd Avenue North, St. Petersburg, FL')))
    # result2 = json.loads(result)
    # latitude = result2[0]['geometry']['location']['lat']
    # longitude = result2[0]['geometry']['location']['lng']
    # context = {
    #     'result':result,
    #     'latitude':latitude,
    #     'longitude':longitude,
    #     'key': google_maps_api_key
    # }

    context = {'key': google_maps_api_key}

    return render(request, 'google/geocode.html', context)
    # return JsonResponse(context, safe=False)

def map(request):
    context = {'key': google_maps_api_key}
    # return render(request, 'google/map.html',context)
    return render(request, 'find_investors/index.html',context)


def mydata(request):
    num_bedrooms = request.POST.get('numBedrooms')
    num_bathrooms = request.POST.get('numBathrooms')

    if num_bedrooms == None:
        num_bedrooms = -1.0
    else:
        num_bedrooms = float(num_bedrooms)

    if num_bathrooms == None:
        num_bathrooms = -1.0
    else:
        num_bathrooms = float(num_bathrooms)

    result_list = list(ParcelInfo.objects
                .filter(OWNER__contains='LLC')
                .exclude(ADDR_1__isnull=True)
                .exclude(CITY__isnull=True)
                .exclude(STATE__isnull=True)
                .exclude(ZIP__isnull=True)
                .values('PIN',
                        'FOLIO',
                        'COUNTY',
                        'ADDR_1',
                        'CITY',
                        'STATE',
                        'ZIP',
                        'NUMBER_OF_BEDS',
                        'NUMBER_OF_BATHS',
                        'OWNER'                        
                        ))

    result_list = [x for x in result_list if float(x['NUMBER_OF_BEDS']) > num_bedrooms and float(x['NUMBER_OF_BATHS']) > num_bathrooms]
    result_list = result_list[:600]

    for x in result_list:
        print(x)
  
    #'The Sundial, 2nd Avenue North, St. Petersburg, FL'
    coords = [coordinates(x) for x in result_list]
    coords = [x for x in coords if x != None]

    # context = { **coords[0], 'title': 'whatever' }

    # context = {
    #     # **get_coordinates(str(result_list[0])),
    #     **get_coordinates('The Sundial, 2nd Avenue North, St. Petersburg, FL'),
    #     'title': '\n'.join(['The Sundial', 'Purchase Price: $1,000,000', 'Sale Price: $3,000,000', 'Owner: Yo Mama']),
    # }

    context = []

    for x in coords:
        context.append(x)

    # context = [{'latitude': 27.7737528, 
    #             'longitude': -82.6344667, 
    #             'title': 'The Sundial\nPurchase Price: $1,000,000\nSale Price: $3,000,000\nOwner: Yo Mama'
    #             }]

    return JsonResponse(context, safe=False)

def set_message(request):
    if request.user.is_authenticated:
        misc_values['msgBody'] = request.POST.get('msgBody')
        misc_values['msgSubject'] = request.POST.get('msgSubject')
        return find_investors(request)

    else:
        return render(request, 'web/landing_page.html')

def find_investors(request):
    return render(request, 'find_investors/index.html', misc_values)
    if request.user.is_authenticated:
        return render(request, 'find_investors/landing_page.html', misc_values)

    else:
        return render(request, 'web/landing_page.html')

