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

    Returns:
    A list of holidays, each represented as a dictionary with the following keys:
    name (str): The name of the holiday.
    date (str): The date of the holiday in the format 'YYYY-MM-DD'.
    description (str): A description of the holiday.
    location (str): The location of the holiday.
    type (str): The type of holiday (e.g. national, regional, local).
    language (str): The language of the holiday name and description.
    """
    year = request.GET.get('year', datetime.datetime.now().year)
    country = request.GET.get('country', 'US')
    search_name = request.GET.get('name', '')
    cache_key = f'holidays_{country}_{year}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)
    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}&uuid=true"
    response = requests.get(url)
    data = response.json()['response']['holidays']
    cache.set(cache_key, data, timeout=86400)
    if search_name:
        data = [holiday for holiday in data if search_name.lower() in holiday['name'].lower()]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def holidayDetail(request):
    pass