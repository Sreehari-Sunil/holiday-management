import datetime
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.conf import settings as SETTINGS

API_KEY = SETTINGS.CALENDRIFIC_API_KEY


@api_view(['GET'])
@permission_classes([AllowAny])
def get_holidays(request):
    print(API_KEY)
    year = request.GET.get('year', datetime.datetime.now().year)
    country = request.GET.get('country', 'US')
    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}"
    response = requests.get(url)
    return Response(response.json(), status=status.HTTP_200_OK)