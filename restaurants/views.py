from django.shortcuts import render
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def home(request):
    key = settings.ZOMATO_KEY
    locations = []
    if request.method == 'POST':
        query = request.POST.get('searched')
        payload = {
            'q': query,
            'apikey': key
        }
        response = requests.get(settings.ZOMATO_BASE + 'cities', params=payload)
        print("url = ", response.url)
        print(response.json())
        print(dir(response))
        locations = response.json()['location_suggestions']

    context = {
        'zomato_base': settings.ZOMATO_BASE + 'cities',
        'apikey': key,
        'locations': locations,
    }
    return render(request, 'main/index.html', context)

@login_required(login_url='/admin/login/')
def search(request, cityId, city):
    key = settings.ZOMATO_KEY
    if request.method == 'POST':
        query = request.POST.get('rest_name')
        lat = request.POST.get('lat')
        if not lat:
            lat = ""
        lon = request.POST.get('long')
        if not lon:
            lon = ""
        radius = request.POST.get('radius')
        if not radius:
            radius = 5000
        jump_to = request.POST.get('jump')
        if not jump_to:
            jump_to = 0
        nums = request.POST.get('count')
        if not nums:
            nums = 20
        sort = request.POST.get('sort')
        if not sort:
            sort = 'rating'
        print(sort)
        payload = {
            'entity_id': cityId,
            'entity_type': 'city',    
            'q': query,
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'count': nums,
            'start': jump_to,
            'sort': sort,
            'apikey': key,
        }
        response = requests.get(settings.ZOMATO_BASE + 'search', params=payload)
        try:
            restaurants = response.json()['restaurants']
            res = response.json()['results_found']
        except:
            restaurants = []
            res = 0
    
    else:
        payload = {
            'entity_id': cityId,
            'entity_type': 'city',    
            'apikey': key,
            'count': 20
        }
        response = requests.get(settings.ZOMATO_BASE + 'search', params=payload)
        restaurants = response.json()['restaurants']
        res = response.json()['results_found']

    print(id) 
    context = {
        'id': id,
        'city': city,
        'key': key,
        'restaurants': restaurants,
        'res': res,
    }

    return render(request, 'main/search_rest.html', context)
