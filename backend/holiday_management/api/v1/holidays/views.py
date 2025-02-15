import datetime
import requests
from django.core.cache import cache
from django.conf import settings as SETTINGS
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

API_KEY = SETTINGS.CALENDRIFIC_API_KEY


@api_view(['GET'])
@permission_classes([AllowAny])
def get_holidays(request):
    """
    API endpoint to get the list of holidays in a given year and country.

    Parameters:
    year (int): The year to get the holidays for. Defaults to the current year.
    country (str): The country to get the holidays for. Defaults to 'US'.
    """
    year = request.GET.get('year', datetime.datetime.now().year)
    country = request.GET.get('country', 'US')
    search_name = request.GET.get('name', '')
    cache_key = f'holidays_{country}_{year}'
    cached_data = cache.get(cache_key)
    if cached_data:
        if search_name:
            cached_data = [holiday for holiday in cached_data if search_name.lower() in holiday['name'].lower()]
        return Response(cached_data, status=status.HTTP_200_OK)
    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}&uuid=true"
    response = requests.get(url)
    data = response.json()['response']['holidays']
    cache.set(cache_key, data, timeout=86400)
    if search_name:
        data = [holiday for holiday in data if search_name.lower() in holiday['name'].lower()]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def holidayDetail(request):
    """
    API endpoint to get the details of a given holiday.

    Parameters:
    urlid (str): The urlid of the holiday to get the details for.
    year (int): The year to get the holiday details for. Defaults to the current year.
    country (str): The country to get the holiday details for. Defaults to 'US'.
    """
    
    urlid = request.GET.get('urlid')
    year = request.GET.get('year', datetime.datetime.now().year)
    country = request.GET.get('country', 'US')
    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}"
    cache_key = f'holidays_{country}_{year}_{urlid}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)
    response = requests.get(url)
    data = response.json()['response']['holidays']
    holiday=[holiday for holiday in data if holiday['urlid'] == urlid][0]
    cache.set(cache_key, holiday, timeout=86400)
    return Response(holiday, status=status.HTTP_200_OK)